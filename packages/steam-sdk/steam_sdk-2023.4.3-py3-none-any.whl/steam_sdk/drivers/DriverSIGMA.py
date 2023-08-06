import glob
import os
import subprocess
from pathlib import Path

import pandas as pd
import yaml

from steam_sdk.builders.BuilderSIGMA import BuilderSIGMA
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.parsers.ParserCOMSOLToTxt import ParserCOMSOLToTxt
from steam_sdk.parsers.ParserRoxie import ParserRoxie
from steam_sdk.plotters.PlotterSIGMA import generate_report_from_map2d


class DriverSIGMA:
    """
        Class to drive SIGMA models
    """
    def __init__(self, magnet_name, SIGMA_path='', path_folder_SIGMA=None, path_folder_SIGMA_input=None, verbose=False):
        self.SIGMA_path = SIGMA_path
        self.path_folder_SIGMA = path_folder_SIGMA
        self.path_folder_SIGMA_input = path_folder_SIGMA_input
        self.verbose = verbose
        self.magnet_name = magnet_name
        if path_folder_SIGMA is None:
            self.working_dir_path = os.getcwd()
        else:
            self.working_dir_path = path_folder_SIGMA
        if verbose:            print('path_exe =          {}'.format(SIGMA_path))


    def create_coordinate_file(self, path_map2d, coordinate_file_path):
        """
        Creates a csv file with same coordinates as the map2d.

        :param path_map2d: Map2d file to read coordinates from
        :param coordinate_file_path: Path to csv filw to be created
        :return:
        """
        df = pd.read_csv(path_map2d, delim_whitespace=True)
        df_new = pd.DataFrame()
        df_new["X-POS/MM"] = df["X-POS/MM"].apply(lambda x: x / 1000)
        df_new["Y-POS/MM"] = df["Y-POS/MM"].apply(lambda x: x / 1000)
        df_new.to_csv(coordinate_file_path, header=None, index=False)

    def export_B_field_txt_to_map2d(self, path_map2d_roxie, path_result_txt_Bx, path_result_txt_By, path_new_file):
        """
        Copy content of reference map2d file and overwrites Bx and By values which are replaced values from
        comsol output txt file and writes to a new map2d file.
        :param path_map2d: Path to reference map2d from which all values apart from Bx and By is copied from
        :param path_result: Comsol output txt file with evaluated B-field
        :param path_new_file: Path to new map2d file where new B-field is stored
        :return:
        """
        df_reference = pd.read_csv(path_map2d_roxie, delim_whitespace=True)
        with open(path_result_txt_Bx) as file:  # opens a text file
            lines = [line.strip().split() for line in file if not "%" in line]  # loops over each line

        df_txt_Bx = pd.DataFrame(lines, columns=["x", "y", "Bx"])

        df_txt_Bx = df_txt_Bx.apply(pd.to_numeric)

        with open(path_result_txt_By) as file:  # opens a text file
            lines = [line.strip().split() for line in file if not "%" in line]  # loops over each line

        df_txt_By = pd.DataFrame(lines, columns=["x", "y", "By"])
        df_txt_By = df_txt_By.apply(pd.to_numeric)

        # Verify all evaluate field at same coordinates!

        x_tol, y_tol = 1e-10, 1e-10
        x_ref, y_ref = df_reference['X-POS/MM'] / 1000, df_reference['Y-POS/MM'] / 1000

        if ((x_ref - df_txt_Bx['x']).abs().max() < x_tol) and \
                ((x_ref - df_txt_By['x']).abs().max() < x_tol) and \
                ((y_ref - df_txt_Bx['y']).abs().max() < y_tol) and \
                ((y_ref - df_txt_By['y']).abs().max() < y_tol):
            print("All dataframes have the same x and y coordinates.")
        else:
            raise ValueError("Error: Not all dataframes have the same x and y coordinates. Can't compare map2ds!")

        # Create new map2d
        with open(path_new_file, 'w') as file:
            file.write("  BL.   COND.    NO.    X-POS/MM     Y-POS/MM    BX/T       BY/T"
                       "      AREA/MM**2 CURRENT FILL FAC.\n\n")
            content = []
            for index, row in df_reference.iterrows():
                bl, cond, no, x, y, Bx, By, area, curr, fill, fac = row
                bl = int(bl)
                cond = int(cond)
                no = int(no)
                x = f"{x:.4f}"
                y = f"{y:.4f}"
                Bx = df_txt_Bx["Bx"].iloc[index]
                Bx = f"{Bx:.4f}"
                By = df_txt_By["By"].iloc[index]
                By = f"{By:.4f}"
                area = f"{area:.4f}"
                curr = f"{curr:.2f}"
                fill = f"{fill:.4f}"
                content.append(
                    "{0:>6}{1:>6}{2:>7}{3:>13}{4:>13}{5:>11}{6:>11}{7:>11}{8:>9}{9:>8}\n".format(bl, cond, no, x, y, Bx,
                                                                                                 By,
                                                                                                 area, curr, fill))
            file.writelines(content)

    @staticmethod
    def export_all_txt_to_concat_csv():
        """
        Export 1D plots vs time to a concatenated csv file. This file can be utilized with the Viewer.
        :return:
        """
        keyword = "all_times"
        files_to_concat = []
        for filename in os.listdir():
            if keyword in filename:
                files_to_concat.append(filename)
        df_concat = pd.DataFrame()
        for file in files_to_concat:
            df = ParserCOMSOLToTxt().loadTxtCOMSOL(file, header=["time", file.replace(".txt", "")])
            df_concat = pd.concat([df_concat, df], axis = 1)
            df_concat= df_concat.loc[:, ~df_concat.columns.duplicated()]
            print(df_concat)
        df_concat=df_concat.reset_index(drop=True)
        df_concat.to_csv("SIGMA_transient_concat_output_1234567890MF.csv", index = False)



    def run_SIGMA(self, concat_time_frames = True, create_figures=True):
        """
        Run the BuilderSigma with given params.
        :param concat_time_frames:???
        :return:
        """
        current_path = Path(__file__).parent
        path = Path.joinpath(current_path.parent.parent, 'tests', 'builders', 'model_library',
                             'magnets', self.magnet_name, 'input')
        init_dir = os.getcwd()

        working_dir_path = os.path.join(init_dir, self.magnet_name)
        # Check if folder exists:
        if os.path.exists(working_dir_path):
            print("Directory already exists.")
        else:
            os.mkdir(working_dir_path)
        path_map2d_roxie = os.path.join(path, f"{self.magnet_name}.map2d")
        path_result_txt_Bx = os.path.join(self.working_dir_path, 'mf.Bx.txt')
        path_result_txt_By = os.path.join(self.working_dir_path, 'mf.By.txt')
        path_new_file = os.path.join(self.working_dir_path, 'B_field_map2d.map2d')
        print(self.working_dir_path)
        os.chdir(self.working_dir_path)

        batch_file_path = os.path.join(self.working_dir_path, f"{self.magnet_name}_Model_Compile_and_Open.bat")
        print(f'Running Comsol model via: {batch_file_path}')
        subprocess.call(batch_file_path)
        # proc = subprocess.Popen([batch_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # (stdout, stderr) = proc.communicate()
        #
        # if proc.returncode != 0:
        #     print(stderr)
        # else:
        #     print(stdout)
        if concat_time_frames:
            self.export_all_txt_to_concat_csv()

        if create_figures:
            self.export_B_field_txt_to_map2d(path_map2d_roxie, path_result_txt_Bx, path_result_txt_By, path_new_file)
            generate_report_from_map2d(True, path_map2d_roxie, "Roxie Data", path_new_file, "SIGMA DATA", "coil")
