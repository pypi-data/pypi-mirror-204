import csv
import warnings
import math
from scipy.optimize import fsolve
import numpy as np
import pandas as pd
import steammaterials
from steammaterials.STEAM_materials import STEAM_materials
import os
import yaml
from typing import List, Dict

from steam_sdk.data.DataParsimConductor import DataParsimConductor, IcMeasurement, Coil
from steam_sdk.parsers.ParserMap2d import getParametersFromMap2d
from steam_sdk.utils.get_attribute_type import get_attribute_type
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.rhasattr import rhasattr
from steam_sdk.utils.sgetattr import rsetattr, rgetattr
from steam_sdk.data.DataParsimConductor import ConductorSample
from steam_sdk.utils.parse_str_to_list import parse_str_to_list


class ParsimConductor:
    """

    """

    def __init__(self, model_data, groups_to_coils, groups_to_coil_length, dict_coilName_to_conductorIndex, verbose: bool = True):
        """
        If verbose is read to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.model_data = model_data
        self.dict_coilName_to_conductorIndex = dict_coilName_to_conductorIndex
        self.groups_to_coils = groups_to_coils

        # groups_to_coil_length is either None (coil_length will be optimized) or dict (fCu will be optimized)
        self.number_of_groups = max([max(values) for values in self.groups_to_coils.values()])
        if groups_to_coil_length and type(groups_to_coil_length) == float:
            expected_group_numbers = list(range(1, self.number_of_groups + 1))
            self.groups_to_coil_length = {groups_to_coil_length: expected_group_numbers}
        else:
            self.groups_to_coil_length = groups_to_coil_length

        # check input: coil names in groups_to_coils and dict_coilName_to_conductorIndex have to be the same
        if not set(groups_to_coils.keys()) == set(dict_coilName_to_conductorIndex.keys()):
            raise Exception(f'Coils of input dictionaries dont have the same names.')

        # DataParsimConductor object that will hold all the information from the input csv file
        self.data_parsim_conductor = DataParsimConductor()

    def read_from_input(self, path_input_file: str, magnet_name: str, strand_critical_current_measurements: Dict[str, Dict]):
        '''
        Read a .csv file and assign its content to a instance of DataParsimConductor().

        Parameters:
            path_input_file: Path to the .csv file to read
            magnet_name: name of the magnet that should be changed
            strand_critical_current_measurements: dict of all the critical current measurements details specified by the user
        '''

        # read table into pandas dataframe
        if path_input_file.endswith('.csv'):
            df_coils = pd.read_csv(path_input_file)
        elif path_input_file.endswith('.xlsx'):
            df_coils = pd.read_excel(path_input_file)
        else:
            raise Exception(f'The extension of the file {path_input_file} is not supported. Use either csv or xlsx.')
        df_coils = df_coils.dropna(axis=1, how='all')

        # read dict for reading columns into local dataclass
        yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translation_dicts", "conductor_column_names.yaml")
        with open(yaml_path, 'r') as file:
            dict_attribute_to_column = yaml.safe_load(file) # TODO discuss with mariusz and implement also in ParsimEventMagnet

        # set magnet name to local model
        rsetattr(self.data_parsim_conductor, 'GeneralParameters.magnet_name', magnet_name)

        # get column name of coil and magnet
        parsed_columns = []  # list containing the column names that were parsed
        column_name_magnets, column_name_coils = self.__get_and_check_main_column_names(df_coils, parsed_columns, dict_attribute_to_column['MainColumnNames'])

        # delete all rows of dataframe that don't belong to the magnet
        mask = df_coils[column_name_magnets] != magnet_name  # create a boolean mask for the rows that do not have the value in the column
        df_coils = df_coils.drop(df_coils[mask].index)  # drop the rows that do not have the value in the column

        # Assign the content to a dataclass structure - loop over all the coils of the magnet in the database
        for _, row in df_coils.iterrows():
            self.__read_magnet(row, column_name_coils, parsed_columns)
            self.__read_coils(row, column_name_coils, parsed_columns, dict_attribute_to_column['Coil'])
            self.__read_conductors(row, column_name_coils, parsed_columns, strand_critical_current_measurements,
                                   dict_attribute_to_column['ConductorSample'])

        # show the user all the columns that where ignored by the code
        ignored_column_names = list(set(df_coils.columns) - set(parsed_columns))
        if self.verbose: print(f'Names of ignored columns: {ignored_column_names}')

    def write_conductor_parameter_file(self, path_output_file: str, simulation_name: str, simulation_number: int):
        """
        Write the Parsim Conductor information to a CSV file, that can be used to run a ParsimSweep Step.

        Parameters:
            path_output_file (str): path to the output file
            groups_to_coil_length: None, float or dict
        """

        # Make target folder if it is missing
        make_folder_if_not_existing(os.path.dirname(path_output_file))

        # save all conductor parameters in a dict
        dict_sweeper = dict()
        dict_sweeper['simulation_name'] = simulation_name
        dict_sweeper['simulation_number'] = int(simulation_number)

        # write all the ConductorSample data to
        if self.groups_to_coil_length:
            # if groups_to_coil_length is specified, optimize the fraction of superconductor
            self.__write_parsweep_conductors(dict_sweeper, flag_optimize_fCu=True)
        else:
            # if no groups_to_coil_length is specified, optimize the length of the magnet
            self.__write_parsweep_conductors(dict_sweeper, flag_optimize_fCu=False)
            # self.__write_parsweep_optimized_ht_length(dict_sweeper)

        # open file in writing mode and write the dict of the parameters as a row in the sweeper csv file
        with open(path_output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=dict_sweeper.keys())
            writer.writeheader()
            writer.writerow(dict_sweeper)

    ################ HELPERS

    def __get_and_check_main_column_names(self, df_coils, parsed_columns, dict_attr_to_colname):
        '''
            TODO refactoring and docstrings
        '''
        # allowed names for the magnet
        csv_column_names_for_magnet_name = dict_attr_to_colname['magnet_name']
        csv_column_names_for_coil_name = dict_attr_to_colname['coil_name']

        # find out what name is being used for the magnet and coil column
        column_name_magnets, column_name_coils = None, None
        for col_name_magnet in csv_column_names_for_magnet_name:
            if col_name_magnet in df_coils.keys():
                column_name_magnets = col_name_magnet
        for col_name_coil in csv_column_names_for_coil_name:
            if col_name_coil in df_coils.keys():
                column_name_coils = col_name_coil
        # TODO do i check later if coilnames are valid?

        # check if there is a column for magnet and coil
        if not column_name_magnets:
            raise Exception(f'No column for the magnet name could be found in the input table. Make sure this column is present.\nAllowed values :{csv_column_names_for_magnet_name}')
        if not column_name_coils:
            raise Exception(f'No column for the coil names could be found in the input table. Make sure this columns are present.\nAllowed values:{csv_column_names_for_coil_name}')

        # check if magnet name is present in the xlsx file
        if not any(df_coils[column_name_magnets] == self.data_parsim_conductor.GeneralParameters.magnet_name):
            raise Exception(f'The magnet "{self.data_parsim_conductor.GeneralParameters.magnet_name}" is not present in the conductor database. ')

        # mark columns as parsed
        parsed_columns.append(column_name_magnets)
        parsed_columns.append(column_name_coils)

        return column_name_magnets, column_name_coils

    def __read_magnet(self, row, column_name_coils, parsed_columns):
        # add coil name to Coils list
        self.data_parsim_conductor.Magnet.coils.append(row[column_name_coils])
        
    def __read_coils(self, row, column_name_coils, parsed_columns, dict_attr_to_colname):
        # create new coil instance
        coil_name = row[column_name_coils]
        new_Coil = Coil()

        # change parameters of coil instance according to yaml translation file
        for attribute_name, column_names in dict_attr_to_colname.items():
            # check if only one column for the attribute can be found
            used_column_names = [entry for entry in column_names if entry in row]
            if len(used_column_names) == 1:
                used_column_name = used_column_names[0]
            elif len(used_column_names) == 0:
                warnings.warn(f'No column for Coil attribute "{attribute_name}" found.')
                continue
            else: raise ValueError(f"More then one column for the ConductorSample attribute '{attribute_name}' found.")

            # check dimension of input column to convert number into SI unit
            dim = used_column_name[used_column_name.find('[') + 1:used_column_name.find(']')] if '[' in used_column_name else ''
            # check if value is set in csv file
            if not pd.isna(row[used_column_name]):
                # if input is a float list in string format, parse it into a float list
                if get_attribute_type(new_Coil, attribute_name)[0] == List[float]:
                    if isinstance(row[used_column_name], str):
                        float_list = parse_str_to_list(row[used_column_name], only_float_list=True)
                    else:
                        float_list = [row[used_column_name]]
                    rsetattr(new_Coil, attribute_name, [make_value_SI(val, dim) for val in float_list])
                else:
                    # change parameter and convert number into SI unit
                    rsetattr(new_Coil, attribute_name, make_value_SI(row[used_column_name], dim))
                # mark column as parsed
                if used_column_name not in parsed_columns: parsed_columns.append(used_column_name)

        self.data_parsim_conductor.Coils[coil_name] = new_Coil

    def __read_conductors(self, row, column_name_coils, parsed_columns, strand_critical_current_measurements, dict_attr_to_colname):
        '''
        Function to read ConductorSamples of ParsimConductors

        :param row: Series of parameters (read from csv file)
        :param parsed_columns: list of parsed table columns names
        '''
        coil_name = row[column_name_coils]

        # read how many conductor samples there are in the database for this coil
        n_conductor_samples_found = []
        all_col_names = [string for string_list in dict_attr_to_colname.values() for string in string_list]
        # add column names for Ic measurements
        for meas in strand_critical_current_measurements:
            if coil_name in meas.coil_names:
                all_col_names.append(meas.column_name_I_critical)
                all_col_names.append(meas.column_name_CuNoCu_short_sample)
        for col_name in all_col_names:
            if col_name in row and not pd.isna(row[col_name]) and isinstance(row[col_name], str):
                float_list = parse_str_to_list(row[col_name], only_float_list=True)
                n_conductor_samples_found.append(len(float_list))
        if all(element == n_conductor_samples_found[0] for element in n_conductor_samples_found):
            n_conductor_samples = n_conductor_samples_found[0]
        else:
            raise Exception(f'Different number of Conductor Samples found for Coil "{coil_name}".')

        # check length of weight factors
        if self.data_parsim_conductor.Coils[coil_name].weight_factors:
            if len(self.data_parsim_conductor.Coils[coil_name].weight_factors) != n_conductor_samples:
                raise Exception(f'Length of weight factor for coil {coil_name} is not similar to number of Conductor samples. Please correct the length to {n_conductor_samples} or delete entry (the average of the values will then be calculated)')

        # create ConductorSample instances for every conductor sample
        new_Conductors = [ConductorSample() for _ in range(n_conductor_samples)]

        # read the critical current measurements into instances of the local conductor sample dataclasses
        for meas in strand_critical_current_measurements:
            # raise error when col name of IcMeasurement is in translation dictionary (meaning it is already used)
            for attr_name, col_names in dict_attr_to_colname.items():
                if meas.column_name_I_critical in col_names:
                    raise Exception(f'Invalid column name for I_critical. "{meas.column_name_I_critical}" already used for the attribute "{attr_name}". Please change.')
                if meas.column_name_CuNoCu_short_sample in col_names:
                    raise Exception(f'Invalid column name for I_critical. "{meas.column_name_CuNoCu_short_sample}" already used for the attribute "{attr_name}". Please change.')

            if coil_name in meas.coil_names:
                # create new IcMeasurement instances, add all values and append it to the measurement list of the conductor
                new_Ic_measurements = [IcMeasurement() for _ in range(n_conductor_samples)]
                  # TODO falsch - ConductorSample braucht list of IcMeasurement
                # add temperature and magnetic flux of the measurements (directly given in step definition)
                for Ic_meas in new_Ic_measurements:
                    rsetattr(Ic_meas, 'B_ref_Ic', meas.reference_mag_field)
                    rsetattr(Ic_meas, 'T_ref_Ic', meas.reference_temperature)
                # read critical current form csv file
                if meas.column_name_I_critical in row and not pd.isna(row[meas.column_name_I_critical]):
                    setattr_to_list(new_Ic_measurements, row, meas.column_name_I_critical, 'Ic')
                else:
                    raise Exception(f'Provided coulumn name for Ic measurement "{meas.column_name_I_critical}" was not found in the conductor database or is empty for coil {coil_name}.')
                # read CuNoCu ratio of the short sample measurement
                if meas.column_name_CuNoCu_short_sample in row and not pd.isna(row[meas.column_name_CuNoCu_short_sample]):
                    setattr_to_list(new_Ic_measurements, row, meas.column_name_CuNoCu_short_sample, 'Cu_noCu_sample')
                else:
                    raise Exception(f'Provided coulumn name for Ic measurement "{meas.column_name_CuNoCu_short_sample}" was not found in the conductor database or is empty.')
                # append the new Ic measurements to a conductor sample
                for cond, Ic_meas in zip(new_Conductors, new_Ic_measurements):
                    cond.Ic_measurements.append(Ic_meas)

        # change parameters of conductors instance according to yaml translation file
        for attribute_name, column_names in dict_attr_to_colname.items():
            # check if only one column for the attribute can be found
            used_column_names = [entry for entry in column_names if entry in row]
            if len(used_column_names) == 1:
                used_column_name = used_column_names[0]
            elif len(used_column_names) == 0:
                warnings.warn(f'No column for ConductorSample attribute "{attribute_name}" found.')
                continue
            else: raise ValueError(f"More then one column for the ConductorSample attribute '{attribute_name}' found.")

            # check if value is set in csv file and set it to all the conductor instances
            if not pd.isna(row[used_column_name]):
                setattr_to_list(new_Conductors, row, used_column_name, attribute_name)
            # mark column as parsed
            if used_column_name not in parsed_columns: parsed_columns.append(used_column_name)

        # check if only either diameter or bare w/h is set and check if original conductor type is the right one
        original_conductor_type = self.model_data.Conductors[self.dict_coilName_to_conductorIndex[coil_name]].strand.type
        if not original_conductor_type: raise Exception(f'Strand type of conductor in coil {coil_name} is not specified in modelData.')
        for cond in new_Conductors:
            if original_conductor_type == 'Round':
                if cond.strand_geometry.bare_width or cond.strand_geometry.bare_height:
                    raise Exception(f'Tried to change bare with/height of Round coil named {coil_name}')
            elif original_conductor_type == 'Rectangular':
                if cond.strand_geometry.diameter:
                    raise Exception(f'Tried to change diameter of Rectangular coil named {coil_name}')
            else:
                raise Exception(f'Unknown conductor type {original_conductor_type} for for coil {coil_name}.')

        # append new conductor instance to Conductors dictionary of ParsimConductor
        self.data_parsim_conductor.Coils[coil_name].conductorSamples = new_Conductors


    def __write_parsweep_optimized_ht_length(self, dict_sweeper):
        # create empty list to later fill with optimized values
        half_turn_length = [None for _ in range(self.number_of_groups)]

        # looping through the coil list
        for coil_name, coil in self.data_parsim_conductor.Coils.items():
            original_conductor = self.model_data.Conductors[self.dict_coilName_to_conductorIndex[coil_name]]
            for index in self.groups_to_coils[coil_name]:
                for sample in coil.conductorSamples:
                    half_turn_length[index-1] = self.optimize_coil_length_with_resistance_meas(sample, original_conductor, dict_sweeper)

        # raise Exception if there is still a None value in half_turn_length
        if not all(item is not None for item in half_turn_length):
            raise Exception('Something went wrong when calculating the half_turn_length. Not every list entry could be calculated.')

        # add the list to the sweeper dict as a string
        dict_sweeper[f'CoilWindings.half_turn_length'] = '[' + ', '.join(str(x) for x in half_turn_length) + ']'  # TODO test if this works with ParsimSweeper in AnalysisSTEAM

    # TODO correction factor strand twist-pitch: f_twist_pitch = sqrt(wBare^2+(Lp_s/2)^2)/(Lp_s/2) , where w=wBare cable width, Lp_s=strand twist-pitch; if set to 2, take into account the increases of electrical resistance, ohmic loss per unit length, inter-filament and inter-strand coupling loss per unit length, and fractions of superconductor and stabilizer in the cable bare cross-section due to strand twist-pitch (default=0)
    # R = C_rho_Cu_NIST_fit with the coil_resistance_room_T, T_ref_coil_resistance and RRR (between 273 and 4) - most people take between RT and 4K


    # def optimize_coil_length_with_resistance_meas(self, conductor_sample, conductor_samples, weight_factors, original_conductor):
    #     # calculate correction factor strand twist-pitch with bare cable width and strand twist pitch
    #     bare_cable_width = getattr_from_list(conductor_samples, 'bare_cable_width', weight_factors=weight_factors)
    #     if not bare_cable_width: bare_cable_width = original_conductor.cable.bare_cable_width
    #
    #     f_twist_pitch = self.calculate_f_twist_pitch(conductor_sample, conductor_samples, original_conductor)
    #
    #     # get number of half turns from map2d file if present
    #     if self.model_data.Sources.magnetic_field_fromROXIE:
    #         path_map2d = self.model_data.Sources.magnetic_field_fromROXIE
    #         number_of_ht, _, _, _, _, _, _, _ = getParametersFromMap2d(map2dFile=path_map2d) # TODO test this in AnalysisSTEAM
    #     else:
    #         number_of_ht = self.model_data.CoilWindings.n_half_turn_in_group
    #
    #     # define function to solve
    #     def resistance_as_function_of_L(L, *args):
    #         fCu, A_cond, temperature, mag_field, RRR, Tup_RRR  = args  # unpack arguments
    #         rho_parameters = np.vstack((temperature, mag_field, RRR, Tup_RRR))  # create parameter v stack for c function
    #         matpath = os.path.dirname(steammaterials.__file__)
    #         CFUN_rhoCuNIST = STEAM_materials('CFUN_rhoCuNIST', rho_parameters.shape[0], rho_parameters.shape[1], matpath)
    #         rho = CFUN_rhoCuNIST.evaluate(rho_parameters)[0]
    #         return rho * L / (fCu * A_cond) * f_twist_pitch  # TODO solve it analytically
    #
    #     # define parameters needed for function
    #     fCu = conductor_sample.Cu_noCu_resistance_meas / (1 + conductor_sample.Cu_noCu_resistance_meas)  # TODO if not present modeldata
    #     key_RRR = f'Conductors[{conductor_sample.index_of_conductor_in_modelData}].strand.RRR'
    #     if key_RRR in dict_sweeper:
    #         RRR = dict_sweeper[key_RRR]  # use RRR from database - if not existing use modelData
    #         Tup_RRR  = ...#TODO Cond.T_ref_RRR_high if not use 293.0
    #     else:
    #         if not original_conductor.strand.RRR: raise Exception('TODO')
    #         if not original_conductor.strand.T_ref_RRR_high: raise Exception('TODO')
    #         RRR = original_conductor.strand.RRR
    #         Tup_RRR = original_conductor.strand.T_ref_RRR_high
    #     A_cond = calc_strand_area(strand_geometry=conductor_sample.strand_geometry, original_conductor=original_conductor) # TODO is this right? * n_strands
    #     temperature = ...#TODO Cond.coil_resistance_room_T if not 293.0  # TODO
    #     mag_field = 0
    #       # TODO if measured find in column
    #
    #     # solve equation for magnetic length
    #     args = (fCu, A_cond, temperature, mag_field, RRR, Tup_RRR)
    #     if self.model_data.GeneralParameters.magnetic_length:
    #         initial_guess = [self.model_data.GeneralParameters.magnetic_length]
    #     else: initial_guess = [10]
    #     L = fsolve(func=resistance_as_function_of_L, x0=initial_guess, args=args)
    #     L_ht = L[0] / number_of_ht
    #     return L_ht
    #
    def calculate_f_twist_pitch(self, conductor_sample, dict_sweeper, original_conductor):
        # get the bare_cable_width from the database if it has been changed, if not: use the default one from model_data
        key_bare_cable_width = f'Conductors[{conductor_sample.index_of_conductor_in_modelData}].cable.bare_cable_width'
        if key_bare_cable_width in dict_sweeper:
            bare_cable_width = dict_sweeper[key_bare_cable_width]
        else:
            bare_cable_width = original_conductor.cable.bare_cable_width

        # get the strand_twist_pitch from the database if it has been changed, if not: use the default one from model_data
        key_strand_twist_pitch = f'Conductors[{conductor_sample.index_of_conductor_in_modelData}].cable.strand_twist_pitch'
        if key_strand_twist_pitch in dict_sweeper:
            strand_twist_pitch = dict_sweeper[key_strand_twist_pitch]
        else:
            strand_twist_pitch = original_conductor.cable.strand_twist_pitch
            
        # calculate correction factor strand twist-pitch
        f_twist_pitch = np.sqrt(bare_cable_width ** 2 + (strand_twist_pitch / 2) ** 2) / (strand_twist_pitch / 2)  # TODO should be around 1.03-1.05
        return f_twist_pitch


    def __write_parsweep_conductors(self, dict_sweeper, flag_optimize_fCu: bool):
        """
        Writes the Conductor parameter for a sweeper csv file to a dict.

        Parameters:
        - dict_sweeper (dict): input dict where the sweeper entries will be stored  int the format {columnName: value}
        - flag_optimize_fCu (bool): TODO

        """
        # parameter dict for creating the column names of sweeper csv file
        dict_param = {
            # format {attribute_name_of_ConductorSample_object: attribute_name_of_Conductor_from_DataModelMagnet_object}
            'strand_geometry.diameter': 'strand.diameter',
            'strand_geometry.bare_width': 'strand.bare_width',
            'strand_geometry.bare_height': 'strand.bare_height',
            'RRR': 'strand.RRR',
            'Cu_noCu': 'strand.Cu_noCu_in_strand',
            'width': 'cable.bare_cable_width',
            'filament_twist_pitch': 'strand.fil_twist_pitch',
            'strand_twist_pitch': 'cable.strand_twist_pitch',
# TODO name the attribute_name_of_ConductorSample_object identical to attribute_name_of_Conductor_from_DataModelMagnet_object to not need this dict?
        }

        # looping through the coil list
        for coil_name, coil in self.data_parsim_conductor.Coils.items():
            idx = self.dict_coilName_to_conductorIndex[coil_name]
            sweeper_cond_name = f'Conductors[{idx}].'

            # parse data from DataParsimConductor to strings for sweeper csv and store them in dict_sweeper
            for sample_attribute_name, conductor_attribute_name in dict_param.items():
                val = getattr_from_list(coil.conductorSamples, sample_attribute_name, coil.weight_factors)
                if val:
                    # check if the original conductor has the attribute that will be changed to avoid errors when running parsim sweeper
                    if not rhasattr(self.model_data.Conductors[idx], conductor_attribute_name):
                        raise Exception(f'Tried to change conductor attribute "{conductor_attribute_name}" that is not specified for the conductor of coil {coil_name}.')
                    # append value to sweeper dict
                    dict_sweeper[sweeper_cond_name + conductor_attribute_name] = val

            # insert Jc fit value(s) depending on their fitting function (usual Bottura, CUDI1, CUDI3 for NbTi and Summers, Bordini for Nb3Sn)
            Jc_dict_list = []
            for conductor_sample in coil.conductorSamples:
                # calculate the parameters for Jc fit for every conductor sample of this coil
                Jc_dict = get_Jc_fit_params(original_conductor=self.model_data.Conductors[idx], coil_name=coil_name,
                                  strand_geometry=conductor_sample.strand_geometry, Bc20=conductor_sample.Bc20,
                                  Ic_measurements=conductor_sample.Ic_measurements, Tc0=conductor_sample.Tc0)
                Jc_dict_list.append(Jc_dict)
            # Calculate the average of values for each key across all dictionaries in the list
            Jc_avg_dict = {key: sum(d[key] for d in Jc_dict_list) / len(Jc_dict_list) for key in Jc_dict_list[0]}
            for name, val in Jc_avg_dict.items():
                if val: dict_sweeper[sweeper_cond_name + 'Jc_fit.' + name] = val

            # optimize the fraction of copper with the resistance measurement at room temperature
            # if flag_optimize_fCu:
                # list_optimized_Cu_noCu = []
                # for conductor_sample in coil.conductorSamples:
                #     list_optimized_Cu_noCu.append(self.optimize_fCu_with_resistance_meas(coil.conductorSamples, self.model_data.Conductors[idx], dict_sweeper))
                # dict_sweeper[sweeper_cond_name + 'strand.Cu_noCu_in_strand'] = val

    def optimize_fCu_with_resistance_meas(self, conductor_samples, original_conductor, dict_sweeper):
        # # calculate correction factor strand twist-pitch with bare cable width and strand twist pitch
        # f_twist_pitch = self.calculate_f_twist_pitch(conductor_sample, dict_sweeper, original_conductor)
        #
        # # define function to solve
        # def resistance_as_function_of_fCu(fCu, *args):
        #     L, A_cond, temperature, mag_field, RRR, RRR_ref = args  # unpack arguments
        #     numpy2d = np.vstack((temperature, mag_field, RRR, RRR_ref))  # create parameter v stack for c function
        #     matpath = os.path.dirname(steammaterials.__file__)
        #     CFUN_rhoCuNIST = STEAM_materials('CFUN_rhoCuNIST', numpy2d.shape[0], numpy2d.shape[1], matpath)
        #     rho = CFUN_rhoCuNIST.evaluate(numpy2d)  # TODO check dimension (1x1 array)
        #     return rho * L / (fCu * A_cond) * f_twist_pitch
        #
        # # solve equation for fraction of Copper
        # args = (1, 0.2, 273, 0, 100, 1)  # TODO: copy from optimize_L_with_resistance_meas if working
        # if original_conductor.strand.Cu_noCu_in_strand:
        #     initial_guess = [original_conductor.strand.Cu_noCu_in_strand]
        # else: initial_guess = [0.1]
        # fCu = fsolve(func=resistance_as_function_of_fCu, x0=initial_guess, args=args)
        # Cu_noCu = fCu[0] / (1 - fCu[0])
        # if Cu_noCu < 0.01:
        #     Cu_noCu = 0.01  # TODO delete this and find cause of problem
        # return Cu_noCu
        pass


def get_Jc_fit_params(original_conductor, strand_geometry, Tc0, Bc20, Ic_measurements, coil_name):
    # TODO: use C-python-wrapper functions(see steam-materials-library) - ask Mariusz how to set it up (when it is implemented)
    if original_conductor.Jc_fit.type == 'Summers':
        # check inputs
        if not original_conductor.strand.type: raise Exception(
            f'Strand type of conductor in coil {coil_name} is not specified in modelData.')
        if len(Ic_measurements) > 1:
            # TODO we could solve the overdetermined system of equations with Least Squares algorithms, like numpy.linalg.lstsq
            raise Exception(
                f'More then one Measurement for Summers fit provided for coil {coil_name}. Please only provide 1 or 0.')
        elif len(Ic_measurements) < 1:
            warnings.warn(
                f'No Measurement for Summers fit provided for coil {coil_name}. Calculation of new Summers parameters will be skipped.')
            return {}
        else:
            Ic_measurement = Ic_measurements[0]
            if not Ic_measurement.Ic: raise Exception(
                f'No measured critical current (Ic) for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not Ic_measurement.B_ref_Ic: raise Exception(
                f'No reference magnetic field of critical current measurement for Summers fit provided for coil {coil_name}.')
            if not Ic_measurement.T_ref_Ic: raise Exception(
                f'No reference temperature of critical current measurement for Summers fit provided for coil {coil_name}.')
            if not Ic_measurement.Cu_noCu_sample: raise Exception(
                f'No Cu-nCu-ratio of critical current measurement for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')

        # use parameters of modelData if they are not changed with the conductor database
        if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_Summers
        if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_Summers

        # calculate critical current density from critical current by using the area of
        fCu = Ic_measurement.Cu_noCu_sample / (Ic_measurement.Cu_noCu_sample + 1)
        A = calc_strand_area(strand_geometry, original_conductor)
        A_noCu = A * (1 - fCu)
        Jc_Tref_Bref = Ic_measurement.Ic / A_noCu

        # search for the best C0  # TODO use np.linalg.solve?
        tol = 1e-6  # hardcoded
        if original_conductor.Jc_fit.Jc0_Summers:
            val_range = [original_conductor.Jc_fit.Jc0_Summers / 1000, original_conductor.Jc_fit.Jc0_Summers * 1000]
            print(val_range)
        else:
            val_range = [1e6, 1e14]
        n_iterations = math.ceil(
            np.log((val_range[1] - val_range[0]) / tol) / np.log(10))  # from formula: width/(10**n_iterations) = tol
        for _ in range(n_iterations):
            try_CO_Summers = np.linspace(val_range[0], val_range[1], 10)
            tryJc_Summers = np.zeros(len(try_CO_Summers))
            # calculate Jc for every selected C0 value
            for j in range(len(try_CO_Summers)):
                tryJc_Summers[j] = Jc_Nb3Sn_Summer_new(Ic_measurement.T_ref_Ic, Ic_measurement.B_ref_Ic,
                                                       try_CO_Summers[j], Tc0, Bc20)
            # find indices of the list values that are higher than Jc_Tref_Bref
            tempIdx = np.where(np.array(tryJc_Summers) >= Jc_Tref_Bref)[0]
            if len(tempIdx) == 0: raise Exception('No C0 for Jc Summers fit could be found in specified value range.')
            # set new value range for net iteration
            val_range = [try_CO_Summers[tempIdx[0] - 1], try_CO_Summers[tempIdx[0]]]
            C0 = try_CO_Summers[tempIdx[0] - 1]

        return {
            'Jc0_Summers': C0,
            'Tc0_Summers': Tc0,
            'Bc20_Summers': Bc20,
        }
    elif original_conductor.Jc_fit.type == 'Bordini':
        # TODO use C-function when wrapper is available
        return {
            'C0_Bordini': todo(),
            'alpha_Bordini': todo(),
            'Tc0_Bordini': todo(),
            'Bc20_Bordini': todo(),
        }
    elif original_conductor.Jc_fit.type == 'CUDI1':
        # general equation for CUDI1: Ic = (C1 + C2*B) * (1 - T/Tc0*(1-B/Bc20)^-.59)

        # depending on the number of critical current measurements, use different ways to calculate C1 and C2 parameter
        if len(Ic_measurements) not in [0, 1, 2]:
            # TODO we could solve the overdetermined system of equations with Least Squares algorithms, like numpy.linalg.lstsq
            raise Exception(
                f'More then two measurements for CUDI1 fit provided in coil {coil_name}. Please only provide 2, 1 or 0 measurements.')
        elif len(Ic_measurements) == 2:
            # if two measurements are specified, we have 2 equations and 2 unknowns -> system can be solved

            # check inputs and use parameters of modelData if they are not changed with the conductor database
            for Ic_measurement in Ic_measurements:
                if not Ic_measurement.Ic: raise Exception(f'No measured critical current (Ic) for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
                if not Ic_measurement.B_ref_Ic: raise Exception(f'No reference magnetic field of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
                if not Ic_measurement.T_ref_Ic: raise Exception(f'No reference temperature of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
                # if not Ic_measurement.Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not original_conductor.cable.n_strands: raise Exception(
                'No number of strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Tc0_CUDI1: raise Exception(
                'No Tc0 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Bc20_CUDI1: raise Exception(
                'No Bc02 specified in modelData of the conductor that should be changed.')
            if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_CUDI1
            if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_CUDI1

            # convert critical current of strand to critical current of conductor by multiplying with number of strands
            Ic_cable1 = Ic_measurements[0].Ic  # TODO * original_conductor.cable.n_strands
            Ic_cable2 = Ic_measurements[1].Ic  # TODO * original_conductor.cable.n_strands

            # # # solve system of linear equations: A*x = b - redundant way
            # A = np.array([[1, Ic_measurements[0].B_ref_Ic], [1, Ic_measurements[1].B_ref_Ic]])
            # b_1 = Ic_cable1 / (1 - Ic_measurements[0].T_ref_Ic / Tc0 * (1 - Ic_measurements[0].B_ref_Ic / Bc20) ** -0.59)
            # b_2 = Ic_cable2 / (1 - Ic_measurements[1].T_ref_Ic / Tc0 * (1 - Ic_measurements[1].B_ref_Ic / Bc20) ** -0.59)
            # b = np.array([b_1, b_2])
            # x = np.linalg.solve(A, b,)

            def CUDI1_equation_fixed_ratio(C, *args):
                C1, C2 = C
                Ic1, Ic2, T1, T2, Tc0, B1, B2, Bc20 = args

                eq1 = Ic1 - (C1 + C2 * B1) * (1 - T1 / (Tc0 * (1 - B1 / Bc20) ** 0.59))
                eq2 = Ic2 - (C1 + C2 * B2) * (1 - T2 / (Tc0 * (1 - B2 / Bc20) ** 0.59))

                return [eq1, eq2]

            initial_values = [787.327,
                              -63.073]  # values come from magnet "MQML" in csv file "Strand and cable characteristics"
            args = (Ic_cable1, Ic_cable2, Ic_measurements[0].T_ref_Ic, Ic_measurements[1].T_ref_Ic, Tc0,
                    Ic_measurements[0].B_ref_Ic, Ic_measurements[1].B_ref_Ic, Bc20)
            x = fsolve(func=CUDI1_equation_fixed_ratio, x0=initial_values, args=args)

            if len(x) == 2:
                C1, C2 = x
            else:
                raise Exception(
                    f'No valid solution for CUDI1 fitting parameters C1 and C2 could be found for coil {coil_name}.')
        elif len(Ic_measurements) == 1:
            # if only one measurement is provided use one equation and the ratio of C1 and C2 according to modelData and warn the user
            warnings.warn(
                f'Only one Measurement for CUDI1 fit provided for coil {coil_name}. Ratio of C1 and C2 from modelData is used as a second equation.')

            # check inputs and use parameters of modelData if they are not changed with the conductor database
            if not Ic_measurements[0].Ic: raise Exception(
                f'No measured critical current (Ic) for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not Ic_measurements[0].B_ref_Ic: raise Exception(
                f'No reference magnetic field of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
            if not Ic_measurements[0].T_ref_Ic: raise Exception(
                f'No reference temperature of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
            # if not Ic_measurements[0].Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not original_conductor.cable.n_strands: raise Exception(
                'No number of strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Tc0_CUDI1: raise Exception(
                'No Tc0 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Bc20_CUDI1: raise Exception(
                'No Bc02 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.C1_CUDI1: raise Exception(
                'No C1_CUDI1 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.C2_CUDI1: raise Exception(
                'No C2_CUDI1 specified in modelData of the conductor that should be changed.')
            if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_CUDI1
            if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_CUDI1

            # convert critical current of strand to critical current of conductor by multiplying with number of strands
            Ic_cable = Ic_measurements[
                0].Ic  # TODO why delete this "* original_conductor.cable.n_strands" - in csv we only use n_strands=1

            # try to read C1 over C2 ratio from modelData - if not existing use usual ratio for NbTi superconductors
            if not original_conductor.Jc_fit.C1_CUDI1 or not original_conductor.Jc_fit.C2_CUDI1:
                warnings.warn(
                    f'No C1 or C2 parameter defined in modelData for coil {coil_name}. Using usual ratio for NbTi superconductors.')
                # 787.327 and -63.073 are hardcoded values come from magnet "MQML" in csv file "Strand and cable characteristics"
                # saving signed angle instead of ratio to keep track of signs - tan(angle_C1_C2) = C1/C2
                angle_C1_C2 = math.atan2(787.327,
                                         -63.073)  # atan2 is a tangens calcualtion that also saves the sign of the angle depending on the quadrant
                initial_guess = [787.327, -63.073]
            else:
                angle_C1_C2 = math.atan2(original_conductor.Jc_fit.C1_CUDI1, original_conductor.Jc_fit.C2_CUDI1)
                initial_guess = [original_conductor.Jc_fit.C1_CUDI1, original_conductor.Jc_fit.C2_CUDI1]

            def CUDI1_equation_fixed_ratio(C, *args):
                C1, C2 = C
                Ic, T, Tc0, B, Bc20, angle_C1_C2 = args

                eq1 = Ic - (C1 + C2 * B) * (1 - T / (Tc0 * (1 - B / Bc20) ** 0.59))
                eq2 = C1 - C2 * math.tan(angle_C1_C2)

                return [eq1, eq2]

            # Solve the equation system
            args = (Ic_cable, Ic_measurements[0].T_ref_Ic, Tc0, Ic_measurements[0].B_ref_Ic, Bc20, angle_C1_C2)
            C = fsolve(func=CUDI1_equation_fixed_ratio, x0=initial_guess, args=args)
            C1, C2 = C[0], C[1]

            # old approach with analytical solution
            # # Ic = (C1 + C2*B) * (1 - T/Tc0*(1-B/Bc20)^-.59) where only C1 and C2 are unknown - second equation: tan(angle_C1_C2) = C1/C2
            # C2 = Ic_cable / (1 - Ic_measurements[0].T_ref_Ic / (Tc0 * (1 - Ic_measurements[0].B_ref_Ic / Bc20) ** 0.59)) / (Ic_measurements[0].B_ref_Ic + math.tan(angle_C1_C2))
            # C1 = C2 * math.tan(angle_C1_C2)
        elif len(Ic_measurements) == 0:
            # if no measurement is provided use the usual ratio for NbTi superconductors and scale that value by cross section of superconductor and warn the user
            warnings.warn(
                f'No Measurement for CUDI1 fit provided for coil {coil_name}. Usual ratio for NbTi superconductors of C1 and C2 is used and scaled by cross section of superconductor. Copper-non-copper ratio of magnet model will be used.')

            # check inputs
            if not original_conductor.cable.n_strands: raise Exception(
                'No n_strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.strand.Cu_noCu_in_strand: raise Exception(
                'No n_strands specified in modelData of the conductor that should be changed.')

            # hardcoded values come from magnet "MQML" in csv file "Strand and cable characteristics"
            # NOTE: cab...cable, str...strand, C1_cab = C1_str * nStrands  and  C1_str = C1_str_MB / A_MB * A_thisMagnet
            C1_per_square_meter_of_NbTi = 787.327 / 6.580e-08  # C1_cab/(Cable Section NbTi) #  = strandArea * nStrands * (1-fCu)
            C2_per_square_meter_of_NbTi = -63.073 / 6.580e-08  # C2_cab/(Cable Section NbTi) #  = strandArea * nStrands * (1-fCu)

            # scale it with the cross-section of superconductor
            strand_cross_section = calc_strand_area(strand_geometry, original_conductor)
            fraction_of_superconductor = 1 / (original_conductor.strand.Cu_noCu_in_strand + 1)
            total_NbTi_area = fraction_of_superconductor * strand_cross_section  # TODO why do i have to delete this? "* original_conductor.cable.n_strands" (AH97)
            C1 = C1_per_square_meter_of_NbTi * total_NbTi_area
            C2 = C2_per_square_meter_of_NbTi * total_NbTi_area

        # check if values are real and not imaginary (e.g. when Bc20 is bigger than B_ref_Ic)
        if np.iscomplex(complex(C1)) or np.iscomplex(complex(C2)):
            raise Exception(
                f'When calculating CUDI1 parameters (C1, C2) the values turned out to have an imaginary part. Please check the inputs.')

        return {
            # TODO: shall we add a plausibility check - e.g. if the value will be changed by many orders of magnitude
            'Tc0_CUDI1': Tc0,
            'Bc20_CUDI1': Bc20,
            'C1_CUDI1': C1,
            'C2_CUDI1': C2,
        }
    else:
        raise Exception(
            f'No implementation for fit type "{original_conductor.Jc_fit.type}" defined in ParsimConductor.')


def calc_C0_summers(new_conductor, original_conductor, coil_name):
    # check inputs
    Ic_measurement = new_conductor.Ic_measurements[0]
    if not Ic_measurement.Ic: raise Exception(f'No measured critical current (Ic) for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
    if not Ic_measurement.B_ref_Ic: raise Exception(f'No reference magnetic field of critical current measurement for Summers fit provided for coil {coil_name}.')
    if not Ic_measurement.T_ref_Ic: raise Exception(f'No reference temperature of critical current measurement for Summers fit provided for coil {coil_name}.')
    if not Ic_measurement.Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')

    # use parameters of modelData if they are not changed with the conductor database
    Tc0 = new_conductor.Tc0  # TODO should this be done like this with Tc0, or shall i take the avg before the calculation?
    Bc20 = new_conductor.Bc20
    if not Tc0:
        Tc0 = original_conductor.Jc_fit.Tc0_Summers
    if not Bc20:
        Bc20 = original_conductor.Jc_fit.Bc20_Summers

    # calculate critical current density from critical current
    fCu = Ic_measurement.Cu_noCu_sample / (Ic_measurement.Cu_noCu_sample + 1)
    A = calc_strand_area(new_conductor.strand_geometry, original_conductor)
    A_noCu = A * (1 - fCu)
    Jc_Tref_Bref = Ic_measurement.Ic / A_noCu

    # search for the best C0  # TODO use np.linalg.solve or method to use Jc c-func more easily
    tol = 1e-6  # hardcoded
    if original_conductor.Jc_fit.Jc0_Summers:
        val_range = [original_conductor.Jc_fit.Jc0_Summers / 1000, original_conductor.Jc_fit.Jc0_Summers * 1000]
        print(val_range)
    else:
        val_range = [1e6, 1e14]
    n_iterations = math.ceil(
        np.log((val_range[1] - val_range[0]) / tol) / np.log(10))  # from formula: width/(10**n_iterations) = tol
    for _ in range(n_iterations):
        try_CO_Summers = np.linspace(val_range[0], val_range[1], 10)
        tryJc_Summers = np.zeros(len(try_CO_Summers))
        # calculate Jc for every selected C0 value
        for j in range(len(try_CO_Summers)):
            tryJc_Summers[j] = Jc_Nb3Sn_Summer_new(Ic_measurement.T_ref_Ic, Ic_measurement.B_ref_Ic, try_CO_Summers[j], Tc0, Bc20)
        # find indices of the list values that are higher than Jc_Tref_Bref
        tempIdx = np.where(np.array(tryJc_Summers) >= Jc_Tref_Bref)[0]
        if len(tempIdx) == 0: raise Exception('No C0 for Jc Summers fit could be found in specified value range.')
        # set new value range for net iteration
        val_range = [try_CO_Summers[tempIdx[0] - 1], try_CO_Summers[tempIdx[0]]]
        C0 = try_CO_Summers[tempIdx[0] - 1]
    return C0


def calc_strand_area(strand_geometry, original_conductor):
    # check inputs
    if not original_conductor.strand.type: raise Exception(f'Strand type is not specified in modelData.')
    
    if original_conductor.strand.type == 'Round':

        # if diameter is not changed in conductor database, use the one form modeldata
        if not strand_geometry.diameter: diameter = original_conductor.strand.diameter
        else: diameter = strand_geometry.diameter

        # calculate area of circle
        A = np.pi * diameter ** 2 / 4
    elif original_conductor.strand.type == 'Rectangular':

        # if height/width is not changed in conductor database, use the one form modeldata
        if not strand_geometry.bare_height: h = original_conductor.strand.bare_height
        else: h = strand_geometry.bare_height
        if not strand_geometry.bare_width: w = original_conductor.strand.bare_width
        else: w = strand_geometry.bare_width

        # calculate area of circle
        A = w * h
    else:
        raise Exception(f'Unknown type of conductor strand: {original_conductor.strand.type}!')
    return A


def Jc_Nb3Sn_Summer_new(T, B, C, Tc0, Bc20):
    if T==0: T=0.001
    if B==0: B=0.001
    frac_T = T / Tc0
    if frac_T > 1: frac_T=1
    Bc2 = Bc20 * (1 - frac_T ** 2) * (1 - 0.31 * frac_T ** 2 * (1 - 1.77 * np.log(frac_T)))
    frac_B = B / Bc2
    if frac_B > 1: frac_B = 1
    Jc = C / np.sqrt(B) * (1 - frac_B) ** 2 * (1 - frac_T ** 2)**2
    return Jc


def Jc_Nb3Sn_Bordini(T, B, C0, Tc0_Nb3Sn, Bc20_Nb3Sn, alpha):
    # Critical current density in a Nb3Sn strand, Bordini fit

    # % % % Check all inputs are scalars or vectors
    if not (np.isscalar(T) or np.isscalar(B) or np.isscalar(C0) or np.isscalar(Tc0_Nb3Sn) or np.isscalar(Bc20_Nb3Sn) or np.isscalar(alpha)):
        if not (len(T) == len(B) == len(C0) == len(Tc0_Nb3Sn) == len(Bc20_Nb3Sn) == len(alpha)):
            raise ValueError('All inputs must be scalars or vectors with the same number of elements.')

    nElements = max([len(T), len(B), len(C0), len(Tc0_Nb3Sn), len(Bc20_Nb3Sn), len(alpha)])

    # % % % Check all inputs are scalars or vectors with the same number of elements
    if ((len(T) > 1 and len(T) != nElements) or (len(B) > 1 and len(B) != nElements) or
            (len(C0) > 1 and len(C0) != nElements) or
            (len(Tc0_Nb3Sn) > 1 and len(Tc0_Nb3Sn) != nElements) or
            (len(Bc20_Nb3Sn) > 1 and len(Bc20_Nb3Sn) != nElements) or
            (len(alpha) > 1 and len(alpha) != nElements)):
        raise ValueError('All inputs must be scalars or vectors with the same number of elements.')

    # Modify the input magnetic field
    B = np.abs(B)
    B[B < 0] *= -1
    B[np.abs(B) < 0.001] = 0.001  # very small magnetic field causes numerical problems

    f_T_T0 = T / Tc0_Nb3Sn
    f_T_T0[f_T_T0 > 1] = 1  # avoid values higher than 1
    Bc2 = Bc20_Nb3Sn * (1 - f_T_T0 ** 1.52)
    f_B_Bc2 = B / Bc2
    f_B_Bc2[f_B_Bc2 > 1] = 1  # avoid values higher than 1
    C = C0 * (1 - f_T_T0 ** 1.52) ** alpha * (1 - f_T_T0 ** 2) ** alpha

    Jc_T_B = C / B * f_B_Bc2 ** 0.5 * (1 - f_B_Bc2) ** 2  # [A/m^2]
    return Jc_T_B


def todo():
    #TODO make functions whereever this function is used
    return None

def make_value_SI(val: float, dim: str):
    if dim in ['mm', 'mOhm', 'mV']:
        return val / 1000
    elif dim in ['m', 'T', 'K', 'Ohm', 'V', '', ' ', '-']:
        return val
    elif dim in ['kA', 'kV', 'km']:
        return val * 1000
    elif dim in ['degC']:
        return val + 273.15
    else:
        raise Exception(f'unknown physical unit "{dim}".')

def setattr_to_list(list_instances, row, col_name, attr_name):
    # get dimension from csv column name
    dim = col_name[col_name.find('[') + 1:col_name.find(']')] if '[' in col_name else ''

    # parse str into list or make single float to
    if isinstance(row[col_name], str):
        val_list = parse_str_to_list(row[col_name], only_float_list=True)
    elif type(row[col_name]) in [float, int]:
        val_list = [row[col_name] for _ in range(len(list_instances))]
    else:
        raise Exception(f'Unknown datatype in column "{col_name}".')

    for val, instance in zip(val_list, list_instances):
        rsetattr(instance, attr_name, make_value_SI(val, dim))

def getattr_from_list(conductor_samples, sample_attribute_name, weight_factors):
    # check if attribute is either set in all of the conductor_samples (return weighted values) or in none (return None)
    attr_present = []
    for con in conductor_samples:
        if rgetattr(con, sample_attribute_name): attr_present.append(True)
        else: attr_present.append(False)
    if True in attr_present and False in attr_present:
        raise Exception(f'The attribute "{sample_attribute_name}" is only set in a few instances of the ConductorSample list.')
    if not all(attr_present):
        return None

    # read the values for the specific attribute for all the ConductorSample instances and store them in a list
    val_list = []
    for con in conductor_samples:
        val_list.append(rgetattr(con, sample_attribute_name))

    # if there is no weight_factors specified, weight them equally (average)
    if not weight_factors:
        weight_factors = [1.0 for _ in range(len(conductor_samples))]

    # check if length is the same
    if len(weight_factors) != len(val_list):
        raise Exception(f'The length of the weight factors {len(weight_factors)} is not the same as the number of conductor samples {len(val_list)}.')

    # Normalize the weight_factors
    weight_sum = sum(weight_factors)
    normalized_weights = [w / weight_sum for w in weight_factors]

    # calculate weighting
    return sum([v * w for v, w in zip(val_list, normalized_weights)])




