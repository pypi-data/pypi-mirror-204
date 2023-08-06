import os
import time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import subprocess
from steam_sdk.plotters import PlotterSIGMA as p
from steam_sdk.data import DataRoxieParser as dR
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.parsers.ParserRoxie import arcCenter
from steam_sdk.utils.builder_SIGMA_helpers import *
from steam_pysigma import pysigma as ps
import logging

class BuilderSIGMA:
    """
        Class to generate SIGMA models
    """

    def __init__(self, input_model_data: DataModelMagnet = None,
                 input_roxie_data: dR.RoxieData = None, bh_curve_database: str = None,
                 settings_dict: dict = None, output_path: str = None, flag_build: bool = False, verbose: bool = False):
        """
        Class for making Comsol modle with SIGMA via PySIGMA library
        :param input_model_data:
        :type input_model_data:
        :param input_roxie_data:
        :type input_roxie_data:
        :param bh_curve_database: Full path to ROXIE .bhdata file (the extension could be also .txt)
        :type bh_curve_database: str
        :param settings_dict:
        :type settings_dict:
        :param output_path:
        :type output_path:
        :param flag_build:
        :type flag_build:
        :param verbose:
        :type verbose:
        """
        self.verbose: bool = verbose

        self.model_data: DataModelMagnet = input_model_data
        self.roxie_data: dR.RoxieData = input_roxie_data
        self.bh_curve_database = bh_curve_database
        self.settings_dict: dict = settings_dict
        if output_path:
            self.output_path: str = str(output_path).replace('/', '\\')
        else:
            self.output_path = os.getcwd()

        if (not self.model_data or not self.roxie_data) and flag_build:
            raise Exception('Cannot build model without providing DataModelMagnet and RoxieData')
        elif flag_build:
            self.g = ps.GatewaySIGMA()
            self.a = ps.ArraysSIGMA
            self.max_r: float = 0.1
            self.conductor_name = str
            self.cableParameters = {'cable': {}, 'strand': {}, 'Jc_fit': {}}  # dM.Conductor #self.cablesParameters
            # self.wedge_elements =
            # self.model =
            self.coil = []
            self.elements = {}
            self.coil_areas = []
            self.wedge_areas = []
            self.show_halfTurns = True  # to be provided by the yaml in the future
            self.model_name = f"{self.model_data.GeneralParameters.magnet_name}_Model"
            self.COMSOL_exe_path = Path(self.settings_dict['comsolexe_path']).parent
            self.java_jdk_path = self.settings_dict['JAVA_jdk_path']
            self.COMSOL_compile_path = os.path.join(self.COMSOL_exe_path, 'comsolcompile.exe')  # Change os.join()
            self.COMSOL_batch_path = os.path.join(self.COMSOL_exe_path, 'comsolbatch.exe')
            self.COMSOL_version = os.path.basename(os.path.dirname(self.COMSOL_exe_path.parent.parent)).replace("COMSOL", "")
            if self.COMSOL_version != "60" and self.COMSOL_version != "53a":
                raise Exception("Not supporting any other versions than 6.0 and 5.3a")
            self.model_java_file_path = f"{os.path.join(self.output_path, self.model_name)}.java"
            self.compile_batch_file_path = f"{os.path.join(self.output_path, self.model_name)}_Compile_and_Open.bat"
            self.model_class_file_path = f"{os.path.join(self.output_path, self.model_name)}.class"
            self.split_java_file_path = []
            self.study_type = self.model_data.Options_SIGMA.simulation.study_type
            self.num_qh = self.model_data.Quench_Protection.Quench_Heaters.N_strips
            self.make_batch_mode_executable = self.model_data.Options_SIGMA.simulation.make_batch_mode_executable
            self.generate_study = self.model_data.Options_SIGMA.simulation.generate_study
            self.input_coordinates_path = self.model_data.Options_SIGMA.postprocessing.out_2D_at_points.coordinate_source
            self.cfg = self.g.ConfigSigma()
            self.cfg.setComsolVersion(self.COMSOL_version)  # for sigma_60
            self.cfg.setOutputModelPath(self.model_java_file_path)
            self.cfg.setComsolBatchPath(self.COMSOL_batch_path)
            self.cfg.setComsolCompilePath(self.COMSOL_compile_path)
            self.cfg.setExternalCFunLibPath(self.settings_dict["CFunLibPath"])
            self.cfg.setRunStudy(self.make_batch_mode_executable)
            self.cfg.setNumOfQHs(self.num_qh)
            self.cfg.setStudyType(self.study_type)
            self.cfg.setSymFactor(1)
            if self.model_data.Options_SIGMA.quench_initialization.quench_init_HT is not None:
                array = self.a.convert_list_to_string_array(self.g.gateway, self.model_data.Options_SIGMA.quench_initialization.quench_init_HT)
                self.cfg.setQuenchInitHT(array)
            if self.model_data.Options_SIGMA.quench_initialization.quench_init_heat is not None:
                self.cfg.setQuenchInitHeat(float(self.model_data.Options_SIGMA.quench_initialization.quench_init_heat))
            QHPositions = self.g.gateway.jvm.java.util.ArrayList()
            if self.model_data.Options_SIGMA.quench_heaters.quench_heater_positions is not None:
                for qh in self.model_data.Options_SIGMA.quench_heaters.quench_heater_positions:
                    temp = self.g.gateway.jvm.java.util.ArrayList()
                    for pos in qh:
                        temp.add(pos)
                    QHPositions.add(temp)
                self.cfg.setQHPositions(QHPositions)
            else:
                self.cfg.setQHPositions(None)

            self.srv = self.g.TxtSigmaServer(self.cfg.getOutputModelPath(), self.cfg.getComsolBatchPath(),
                                        self.cfg.getComsolCompilePath())
            self.postprocessing_data = self.model_data.Options_SIGMA.postprocessing
            self.variables2DConverted = self.postprocessing_data.out_2D_at_points.variables # List of all exported variables
            self.time2DConverted = self.postprocessing_data.out_2D_at_points.time  # List of all exported time
            self.variables1DvsTime = self.postprocessing_data.out_1D_vs_times.variables
            self.time1DConverted = self.postprocessing_data.out_1D_vs_times.time
            self.variables1DvsTimeVector = self.postprocessing_data.out_1D_vs_times.variables
            self.timeRange = ", ".join(["range(" + ", ".join(map(str, lst)) + ")" for lst in
                                        self.model_data.Options_SIGMA.time_vector_solution.time_step])
            print(f"Comsol compile path {self.COMSOL_compile_path}")
            print(f"Comsol version {self.COMSOL_version}")
            validate_sigma_model_data(self.model_data, self.g.MPHC)
            self.build_magnet()
            self.save_model_java()
            self.save_compile_and_open_bat()
            #self.plot_magnet()

    def build_magnet(self):
        """
        This function builds a magnet and creates the different domains.

        :return: None
        """
        if self.verbose: print(f"SIGMA started generating {self.model_data.GeneralParameters.magnet_name}")
        self.air_ff_domain()
        self.air_domain()
        self.coil_domain()
        self.iron_yoke_domain()
        self.wedge_domain()
        #self.bh_curve()

    def mirrorXY(self, area):
        """
        This function mirrors a SIGMA area object in x, y and xy. Returns all possible mirroring options.
        :param area:
        :return: area, ar2, ar2.mirrorX(), area.mirrorX()
        """
        ar2 = area.mirrorY()
        return area, ar2, ar2.mirrorX(), area.mirrorX()

    def air_ff_domain(self):
        """
        Function creates air far field domain
        :return: None
        """

        iron = self.roxie_data.iron

        kpc = self.g.Point.ofCartesian(0.0, 0.0)
        for i in iron.key_points:
            max_i = max(iron.key_points[i].x, iron.key_points[i].y)
            if max_i > self.max_r:
                self.max_r = max_i

        kp1 = self.g.Point.ofCartesian(self.max_r * 2 * 0.95, 0.0)
        kp2 = self.g.Point.ofCartesian(0.0, self.max_r * 2 * 0.95)
        kp1_out = self.g.Point.ofCartesian(self.max_r * 2, 0.0)
        kp2_out = self.g.Point.ofCartesian(0.0, self.max_r * 2)
        ln1 = self.g.Line.ofEndPoints(kpc, kp1_out)
        ln2 = self.g.Arc.ofEndPointsCenter(kp1_out, kp2_out, kpc)
        ln3 = self.g.Line.ofEndPoints(kp2_out, kp2)
        ln4 = self.g.Arc.ofEndPointsCenter(kp2, kp1, kpc)

        hyper_areas = self.mirrorXY(self.g.Area.ofHyperLines(
            self.a.create_hyper_line_array(self.g.gateway, tuple([ln1, ln2, ln3, ln4]))))

        arg = []  # elements
        for i, ar in enumerate(hyper_areas):
            arg.append(self.g.Element(f"AFF_El{i}", ar))

        self.air_far_field = self.a.create_element_array(self.g.gateway, tuple(arg))

    def air_domain(self):
        """
        Function creates air domain
        :return: None
        """
        kpc = self.g.Point.ofCartesian(0.0, 0.0)

        self.air = self.a.create_element_array(self.g.gateway, self.g.Element('Air', self.g.Area.ofHyperLines(
            self.a.create_hyper_line_array(self.g.gateway,
                                           self.g.Circumference.ofCenterRadius(kpc, self.max_r * 2 * 0.95)))))

    def iron_yoke_domain(self):
        """
        Function creates iron yoke domain
        :return: None
        """
        iron = self.roxie_data.iron

        keyPointsCOMSOL = {}
        hyperLinesCOMSOL = {}
        hyperAreasCOMSOL = {}

        for i in iron.key_points:
            keyPointsCOMSOL[i] = self.g.Point.ofCartesian(iron.key_points[i].x, iron.key_points[i].y)

        for i in iron.hyper_lines:
            if iron.hyper_lines[i].type == 'line':
                hyperLinesCOMSOL[i] = self.g.Line.ofEndPoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                              keyPointsCOMSOL[iron.hyper_lines[i].kp2])

            elif iron.hyper_lines[i].type == 'arc':
                hyperLinesCOMSOL[i] = self.g.Arc.ofThreePoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp3],
                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp2])

            elif iron.hyper_lines[i].type == 'ellipticArc':
                hyperLinesCOMSOL[i] = self.g.EllipticArc.ofEndPointsAxes(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                                         keyPointsCOMSOL[iron.hyper_lines[i].kp2],
                                                                         iron.hyper_lines[i].arg1,
                                                                         iron.hyper_lines[i].arg2)

            elif iron.hyper_lines[i].type == 'circle':
                hyperLinesCOMSOL[i] = self.g.Circumference.ofDiameterEndPoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp2])
            else:
                raise ValueError('Hyper line {} not supported'.format(iron.hyper_lines[i].type))

        for i in iron.hyper_areas:
            arg = [hyperLinesCOMSOL[j] for j in iron.hyper_areas[i].lines]  # lines for areas
            hyperAreasCOMSOL[i] = self.mirrorXY(self.g.Area.ofHyperLines(
                self.a.create_hyper_line_array(self.g.gateway, tuple(arg))))

        for i in hyperAreasCOMSOL:
            arg = []  # elements
            for j, ar in enumerate(hyperAreasCOMSOL[i]):
                arg.append(self.g.Element(f"IY{iron.hyper_areas[i].material[2:]}_{i}_El{j}", ar))

            self.elements[i] = self.a.create_element_array(self.g.gateway, tuple(arg))

    def cable_domain(self, conductor: str = None):
        """
        Function sets cable characteristics and conductor properties.
        :return: None
        """
        self.g.cable = self.g.Cable()
        self.g.cable.setLabel(conductor)
        self.g.cable.setTop(self.model_data.GeneralParameters.T_initial)
        i = 0
        while conductor != self.model_data.Conductors[i].name:
            i += 1
        for entry in self.model_data.Conductors[i]:
            if entry[0] == 'cable' or entry[0] == 'strand' or entry[0] == 'Jc_fit':
                for key in entry[1]:
                    self.cableParameters[entry[0]][key[0]] = key[1] if key[1] else 0.
        self.g.cable.setwInsulNarrow(self.cableParameters['cable']['th_insulation_along_height'])
        self.g.cable.setwInsulWide(self.cableParameters['cable']['th_insulation_along_width'])
        self.g.cable.setRc(self.cableParameters['cable']['Rc'])
        self.g.cable.setRa(self.cableParameters['cable']['Ra'])
        self.g.cable.setwBare(self.cableParameters['cable']['bare_cable_width'])
        self.g.cable.sethInBare(self.cableParameters['cable']['bare_cable_height_low'])
        self.g.cable.sethOutBare(self.cableParameters['cable']['bare_cable_height_high'])
        self.g.cable.setNoOfStrands(self.cableParameters['cable']['n_strands'])
        self.g.cable.setNoOfStrandsPerLayer(self.cableParameters['cable']['n_strands_per_layers'])
        self.g.cable.setNoOfLayers(self.cableParameters['cable']['n_strand_layers'])
        self.g.cable.setlTpStrand(self.cableParameters['cable']['strand_twist_pitch'])
        self.g.cable.setwCore(self.cableParameters['cable']['width_core'])
        self.g.cable.sethCore(self.cableParameters['cable']['height_core'])
        self.g.cable.setThetaTpStrand(self.cableParameters['cable']['strand_twist_pitch_angle'])
        self.g.cable.setFracFillInnerVoids(self.cableParameters['cable']['f_inner_voids'])
        self.g.cable.setFractFillOuterVoids(self.cableParameters['cable']['f_outer_voids'])

        self.g.cable.setdFilament(self.cableParameters['strand']['filament_diameter'])
        self.g.cable.setDstrand(self.cableParameters['strand']['diameter'])
        self.g.cable.setfRhoEff(self.cableParameters['strand']['f_Rho_effective'])
        self.g.cable.setlTp(self.cableParameters['strand']['fil_twist_pitch'])
        self.g.cable.setRRR(self.cableParameters['strand']['RRR'])
        self.g.cable.setTupRRR(self.cableParameters['strand']['T_ref_RRR_high'])
        self.g.cable.setFracHe(0.)
        self.g.cable.setFracCu(self.cableParameters['strand']['Cu_noCu_in_strand'] /
                               (1 + self.cableParameters['strand']['Cu_noCu_in_strand']))
        self.g.cable.setFracSc(1 / (1 + self.cableParameters['strand']['Cu_noCu_in_strand']))
        if self.cableParameters['Jc_fit']['type'][:4] == 'CUDI':
            self.g.cable.setC1(self.cableParameters['Jc_fit']['C1_' + self.cableParameters['Jc_fit']['type']])
            self.g.cable.setC2(self.cableParameters['Jc_fit']['C2_' + self.cableParameters['Jc_fit']['type']])
        else:
            self.g.cable.setC1(0.)
            self.g.cable.setC2(0.)

        self.g.cable.setCriticalSurfaceFit(self.g.Cable.CriticalSurfaceFitEnum.Ic_NbTi_GSI)
        self.g.cable.setInsulationMaterial(self.g.MatDatabase.MAT_KAPTON)
        self.g.cable.setMaterialInnerVoids(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setMaterialOuterVoids(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setMaterialCore(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setResitivityCopperFit(self.g.Cable.ResitivityCopperFitEnum.rho_Cu_CUDI)

    def coil_domain(self):
        """
        Function creates winding blocks domain
        :return: None
        """
        poles = ()
        for coil_nr, coil in self.roxie_data.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                windings = ()
                for layer_nr, layer in pole.layers.items():
                    for winding_key, winding in layer.windings.items():
                        self.conductor_name = winding.conductor_name
                        # self.cableParameters = self.roxie_data.conductor.conductor[winding.conductor_name].parameters
                        self.cable_domain(conductor=winding.conductor_name) #Overwritten
                        areas = ()
                        currents = ()
                        for block_key, block in winding.blocks.items():
                            currents += (block.current_sign,)
                            # kp0 = self.g.Point.ofCartesian(coil.bore_center.x, coil.bore_center.y)
                            bore = coil.bore_center
                            if(block.block_corners.iH.y >0.0 and block.block_corners.oH.y >0.0 and  block.block_corners.iLA.y >0.0 and block.block_corners.oLA.y>0.0): #?
                                inner, outer = arcCenter(bore, block.block_corners.iH, block.block_corners.oH
                                                     , block.block_corners.iLA, block.block_corners.oLA, diff_radius=None)
                            else:
                                inner, outer = arcCenter(bore, block.block_corners.iLA, block.block_corners.oLA, block.block_corners.iH,
                                                         block.block_corners.oH, diff_radius=None)
                            arg = [self.g.Point.ofCartesian(block.block_corners.iH.x, block.block_corners.iH.y),
                                   self.g.Point.ofCartesian(block.block_corners.iLA.x, block.block_corners.iLA.y),
                                   self.g.Point.ofCartesian(block.block_corners.oLA.x, block.block_corners.oLA.y),
                                   self.g.Point.ofCartesian(block.block_corners.oH.x, block.block_corners.oH.y)]
                            kp0_inner = self.g.Point.ofCartesian(inner[0], inner[1])
                            kp0_outer = self.g.Point.ofCartesian(outer[0], outer[1])
                            areas += (self.g.Area.ofHyperLines(
                                self.a.create_hyper_line_array(self.g.gateway,
                                                               (self.g.Arc.ofEndPointsCenter(arg[1], arg[0], kp0_inner),
                                                                self.g.Line.ofEndPoints(arg[1], arg[3]),
                                                                self.g.Arc.ofEndPointsCenter(arg[2], arg[3], kp0_outer),
                                                                self.g.Line.ofEndPoints(arg[0], arg[2])))),)
                        #self.coil_areas += [areas[0], areas[1]]
                        windings += (self.g.Winding.ofAreas(self.a.create_area_array(self.g.gateway, areas),
                                                            self.a.create_int_array(self.g.gateway, currents),
                                                            winding.conductors_number, winding.conductors_number,
                                                            self.g.cable),) # Parse block_index and halfturn index

                poles += (self.g.Pole.ofWindings(self.a.create_winding_array(self.g.gateway, windings)),)

        self.coil = self.g.Coil.ofPoles(self.a.create_pole_array(self.g.gateway, poles))

    # self.coil_areas = area + areaY
    # coil_areas_mirrored = []
    # for ar in self.coil_areas:
    #     new_ar = ar.mirrorX()
    #     coil_areas_mirrored.append(new_ar)
    # self.coil_areas = self.coil_areas + coil_areas_mirrored

    def wedge_domain(self):
        """
        Function creates inter-block wedges domain
        :return: None
        """
        wedges = self.roxie_data.wedges

        elements = []
        for i in wedges:
            kp0_inner = self.g.Point.ofCartesian(wedges[i].corrected_center.inner.x, wedges[i].corrected_center.inner.y)
            kp0_outer = self.g.Point.ofCartesian(wedges[i].corrected_center.outer.x, wedges[i].corrected_center.outer.y)
            arg = [self.g.Point.ofCartesian(wedges[i].corners.iH.x, wedges[i].corners.iH.y),
                   self.g.Point.ofCartesian(wedges[i].corners.iLA.x, wedges[i].corners.iLA.y),
                   self.g.Point.ofCartesian(wedges[i].corners.oH.x, wedges[i].corners.oH.y),
                   self.g.Point.ofCartesian(wedges[i].corners.oLA.x, wedges[i].corners.oLA.y)]

            area = self.g.Area.ofHyperLines(self.a.create_hyper_line_array(
                self.g.gateway, (self.g.Arc.ofEndPointsCenter(arg[0], arg[1], kp0_inner),
                                 self.g.Line.ofEndPoints(arg[1], arg[3]),
                                 self.g.Arc.ofEndPointsCenter(arg[3], arg[2], kp0_outer),
                                 self.g.Line.ofEndPoints(arg[0], arg[2]))))
            self.wedge_areas += [area]

            elements.append(self.g.Element(f"Wedge_El{i}", area))

        self.wedge_elements = self.a.create_element_array(self.g.gateway, tuple(elements))

    def connect_create_MPH_model(self, domains):
        """
        This function connects to the COMSOL server and creates an MPH model by using the MagnetMPHBuilder.
        It then builds the MPH model with the specified domains and global variables.
        If the study type is "Transient" and there are Quench Heaters present, it also builds a Quench Heater MPH model.

        :param domains: a tuple of domains to be included in the MPH model.
        :return: None
        """

        self.srv.connect(self.cfg.getComsolBatchPath())
        self.model = self.g.MagnetMPHBuilder(self.cfg, self.srv)
        # Create map with I0.
        globalMap = build_global_variables(self.g, self.model_data)
        globalMap.put(self.g.MPHC.LABEL_CLIQ_CURRENT_EXT_INITIAL, f"{self.model_data.Options_LEDET.field_map_files.Iref}")
        #magnet = self.g.Magnet_T0_QH()
        #domains = magnet.getDomains()
        self.model = self.g.MagnetMPHBuilder(self.cfg, self.srv)
        self.model.buildMPH(self.a.create_domain_array(self.g.gateway, tuple(domains)), globalMap, 4, 1)
        if self.study_type=="Transient" and self.cfg.getNumOfQHs() > 0:
            builderQH = self.g.QuenchHeaterMPHBuilder(self.cfg, self.srv)
            self.model.connectToServer()
            builderQH.buildQuenchHeaterMPH()

    def create_results(self, input_coordinates_path, path_to_results):
        """
        Function creates SIGMA result objects to export
        :param input_coordinates_path: path to coordinate file to evaluate 2D variables in.
        :param path_to_results: path to result folder
        :return:
        """
        if self.make_batch_mode_executable:
            for i in range(len(self.variables2DConverted)):
                time_vector_2D = ', '.join(str(x) for x in self.time2DConverted[i])

                self.g.ResultsAPI.create2DResultNode(self.srv, self.cfg, self.variables2DConverted[i], time_vector_2D, f"data {i}",
                                              input_coordinates_path, str(path_to_results))
            if self.study_type == "Transient":
                for j in range(len(self.variables1DvsTime)):
                    self.g.ResultsAPI.create1DResultNodeAllTimes(self.srv, self.cfg, self.variables1DvsTime[j], f"1DExport_{j}", path_to_results)

                for k in range(len(self.variables1DvsTimeVector)):
                    print(self.variables1DvsTimeVector[k], self.time1DConverted[k])

                    time_vector_1D = ', '.join(str(x) for x in self.time1DConverted[k])
                    self.g.ResultsAPI.create1DResultNodeTimeVector(self.srv, self.cfg, self.variables1DvsTimeVector[k], time_vector_1D,
                                                            f"data {i + 1 + k}", path_to_results)
        else:
            pass
            #print("No study run, no results to be exported.")

    def save_model_java(self):
        """
        This function saves a Java file to be used in COMSOL simulation software.

        :return: None
        """
        domains = [self.g.AirFarFieldDomain("AFF", self.g.MatDatabase.MAT_AIR, self.air_far_field)]
        domains += [self.g.AirDomain("AIR", self.g.MatDatabase.MAT_AIR, self.air)]

        orderedElements = list(self.elements)
        # change order of generated domains to override correctly

        for hyper_hole_key, hyper_hole in self.roxie_data.iron.hyper_holes.items():
           index = [orderedElements.index(hyper_hole.areas[0]),
                     orderedElements.index(hyper_hole.areas[1])]
           if index[0] < index[1]:
                orderedElements.insert(index[1], orderedElements.pop(index[0]))

        # MAT_AIR, MAT_COIL, MAT_COPPER, MAT_KAPTON, MAT_GLASSFIBER, MAT_INSULATION_TEST, MAT_STEEL, MAT_IRON1,
        # MAT_IRON2, MAT_VOID, MAT_NULL, MAT_COIL_TEST, MAT_G10

        self.iron_yoke = [
            self.g.IronDomain(self.cfg, i, self.bh_curve_database, self.roxie_data.iron.hyper_areas[i].material, self.elements[i])
            for i in orderedElements]  # domains
        domains += self.iron_yoke
        domains.append(self.g.CoilDomain("CO", self.g.MatDatabase.MAT_COIL, self.coil))

        domains.append(self.g.WedgeDomain("W", self.g.MatDatabase.MAT_COPPER, self.wedge_elements))

        # Create magnet model
        self.connect_create_MPH_model(domains)
        # Create results
        if self.generate_study:
            self.build_study()
            # Define result nodes

            self.create_results(self.input_coordinates_path, self.output_path)
        self.srv.build(self.cfg.getOutputModelPath())
        self.model.save()
        print(f"SIGMA successfully generated: {self.model_java_file_path}")
        time.sleep(0.01)
        with open(self.model_java_file_path) as java_file:

            print("Java file splitting started.")
            max_no_lines = 6e4
            public_indexes = []
            files = []
            content = java_file.readlines()
            for i, line in enumerate(content):
                if "public static" in line:
                    public_indexes += [i]

            no_lines = public_indexes[-1] - public_indexes[0]
            no_files = int(np.ceil(no_lines / max_no_lines))
            max_no_lines = round(no_lines / no_files)
            real_indexes = [public_indexes[i] - public_indexes[0] for i in range(len(public_indexes))]
            closest = [min(real_indexes, key=lambda x: abs(x - max_no_lines * (i + 1))) + public_indexes[0]
                       for i in range(no_files)]
            no_run = [int(content[i][content[i].index('run') + 3:content[i].index('(')]) for i in closest[0:-1]]
            no_run += [int(content[public_indexes[-2]][content[public_indexes[-2]].index('run')
                                                       + 3:content[public_indexes[-2]].index('(')]) + 1]
            additional_lines = {}
            for i in range(no_files):
                file_path = os.path.join(self.output_path, self.model_name)
                files += [open(file_path + '_%d.java' % i, 'w')]
                name = self.model_name + '_%d' % i
                self.split_java_file_path += [f"{os.path.join(self.output_path, self.model_name + '_%d' % i)}"]
                files[i].writelines(content[0:public_indexes[0] - 2] + ['public class ' + name + ' {\n', '\n'])
                if i == 0:
                    files[i].writelines('\tpublic static Model run1(Model mph) {\n')
                    files[i].writelines(content[public_indexes[0] + 2:closest[i]] + ['}\n'])
                    additional_lines[name] = {'start': 2, 'end': no_run[i] - 1}
                elif i + 1 == no_files:
                    files[i].writelines(content[closest[i - 1]:public_indexes[-1]] + ['}\n'])
                    additional_lines[name] = {'start': no_run[i - 1], 'end': len(public_indexes) - 1}
                else:
                    files[i].writelines(content[closest[i - 1]:closest[i]] + ['}\n'])
                    additional_lines[name] = {'start': no_run[i - 1], 'end': no_run[i] - 1}
                files[i].close()

        with open(self.model_java_file_path, 'w') as java_file:
            content = content[0:public_indexes[0] + 2] + ['\n'] + \
                      content[public_indexes[-1]:public_indexes[-1] + 2] + ['\t}\n'] + ['}\n']
            content.insert(public_indexes[0] + 2, '\t\tmph = ' + self.model_name + '_0.run1(mph);\n')
            ll = 1
            for name, item in additional_lines.items():
                for j in range(item['end'] - item['start'] + 1):
                    content.insert(public_indexes[0] + 2 + ll + j,
                                   '\t\tmph = ' + name + '.run' + str(item['start'] + j) + '(mph);\n')
                ll += j + 1
            content.insert(public_indexes[0] + 2 + ll, '\t\treturn mph;\n')
            content.insert(public_indexes[0] + 3 + ll, '\t}\n')
            java_file.writelines(content)
        print(f"BuilderSIGMA successfully saved files: {self.split_java_file_path}")

    def plot_magnet(self):
        """
        Plot blocks and halfturns for the roxie model data
        :return: None
        """
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        ax.set_xlim(0., 0.2)
        ax.set_ylim(-.1, 0.1)
        # p.plot_multiple_areas(ax, self.air_far_field_areas)  # air far field
        # p.plot_multiple_areas(ax, self.air_areas)  # air
        # p.plot_multiple_areas(ax, self.iron_yoke_areas)  # iron yoke
        # p.plot_multiple_areas(ax, self.wedges_areas)  # wedges
        if self.show_halfTurns:
            for coil_nr, coil in self.roxie_data.coil.coils.items():
                for pole_nr, pole in coil.poles.items():
                    for layer_nr, layer in pole.layers.items():
                        for winding_key, winding in layer.windings.items():
                            for block_key, block in winding.blocks.items():
                                for halfTurn_nr, halfTurn in block.half_turns.items():
                                    iH = halfTurn.corners.insulated.iH
                                    iLA = halfTurn.corners.insulated.iLA
                                    oH = halfTurn.corners.insulated.oH
                                    oLA = halfTurn.corners.insulated.oLA
                                    ax.add_line(lines.Line2D([iH.x, iLA.x], [iH.y, iLA.y], color='red'))
                                    ax.add_line(lines.Line2D([oH.x, oLA.x], [oH.y, oLA.y], color='red'))
                                    ax.add_line(lines.Line2D([oLA.x, iLA.x], [oLA.y, iLA.y], color='red'))
                                    ax.add_line(lines.Line2D([iH.x, oH.x], [iH.y, oH.y], color='red'))
        p.plot_multiple_areas(ax, self.coil_areas)
        # p.plot_multiple_areas(ax, self.wedge_areas, color='blue')
        # #
        # ax.set_xlim(-self.input['air']['r'] * self.input['air']['r_ffs'],
        #             self.input['air']['r'] * self.input['air']['r_ffs'])
        # ax.set_ylim(-self.input['air']['r'] * self.input['air']['r_ffs'],
        #             self.input['air']['r'] * self.input['air']['r_ffs'])
        plt.show()

    def save_compile_and_open_bat(self):
        """
        Function writes a .bat file which has to be run to create a COMSOL model.
        :return: None
        """
        print("Excecuting bat file")
        script_lines = []
        class_paths = ''
        for file in self.split_java_file_path:
            script_lines += [f'"{self.COMSOL_compile_path}" -jdkroot "{self.java_jdk_path}" "{file}.java"',
                             f'"{self.java_jdk_path}\\bin\\jar.exe" cf "{file}.jar" "{file}.class"']
            class_paths += f'-classpathadd "{file}.jar" '

        script_lines += [
            f'"{self.COMSOL_compile_path}" -jdkroot "{self.java_jdk_path}" {class_paths}"{self.model_java_file_path}"',
            f'"{self.COMSOL_batch_path}" -inputfile "{self.model_class_file_path}" '
            f'-outputfile "{os.path.join(self.output_path, self.model_data.GeneralParameters.magnet_name)}.mph"']

        with open(self.compile_batch_file_path, "w") as outfile:
            outfile.write("\n".join(str(line) for line in script_lines))
        print(f'BuilderSIGMA successfully saved: {self.compile_batch_file_path}')
        os.chdir(self.output_path)

    def build_study(self):
        """
        If valid study time defined function creates a COMSOL study
        :return: None
        """
        if self.study_type is not None:
            if self.study_type == self.g.MPHC.LABEL_STATIONARY:
                # Add code to create and run study
                self.g.StudyAPI.setNewBasicStationaryStudy(self.srv, self.cfg, "sol1")
            elif (self.study_type == self.g.MPHC.LABEL_TRANSIENT):
                self.g.StudyAPI.setNewMonolithicStudy(self.srv, self.cfg, "Default_study", self.timeRange)
            else:
                ValueError("Invaid study_type input")


