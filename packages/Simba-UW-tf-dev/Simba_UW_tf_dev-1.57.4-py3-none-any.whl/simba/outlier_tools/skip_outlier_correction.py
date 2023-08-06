from simba.read_config_unit_tests import (check_file_exist_and_readable,
                                          read_config_file,
                                          read_project_path_and_file_type)
import os, glob
import pandas as pd
from simba.drop_bp_cords import getBpNames, get_fn_ext
from simba.rw_dfs import read_df, save_df
from simba.enums import Paths
from simba.train_model_functions import insert_column_headers_for_outlier_correction
from simba.utils.printing import stdout_success
from simba.utils.warnings import DataHeaderWarning

class OutlierCorrectionSkipper(object):
    """
    Class for skipping outlier correction in SimBA projects.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format

    Notes
    ----------

    Examples
    ----------
    >>> outlier_correction_skipper = OutlierCorrectionSkipper(config_path='MyProjectConfig')
    >>> outlier_correction_skipper.skip_outlier_correction()

    """
    def __init__(self,
                 config_path: str):
        self.config = read_config_file(config_path)
        self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
        self.bp_file_path = os.path.join(self.project_path, Paths.BP_NAMES.value)
        self.in_dir = os.path.join(self.project_path, Paths.INPUT_CSV.value)
        self.out_dir = os.path.join(self.project_path, Paths.OUTLIER_CORRECTED.value)
        if not os.path.exists(self.out_dir): os.makedirs(self.out_dir)
        check_file_exist_and_readable(self.bp_file_path)
        self.x_cols, self.y_cols, self.p_cols = getBpNames(config_path)
        self.header_line = []
        for cols in zip(self.x_cols, self.y_cols, self.p_cols):
            self.header_line.extend((list(cols)))
        self.files_found = glob.glob(self.in_dir + '/*.' + self.file_type)
        print('Processing {} file(s)...'.format(str(len(self.files_found))))

    def skip_outlier_correction(self):
        """
        Standardizes pose-estimation data (i.e., headers) from different pose-estimation packages.
        Results are stored in the project_folder/csv/outlier_corrected_movement_location` directory of
        the SimBA project
        """

        self.file_cnt = 0
        for file_cnt, file_path in enumerate(self.files_found):
            _, video_name, ext = get_fn_ext(file_path)
            data_df = read_df(file_path, self.file_type)
            if self.file_type == 'csv':
                try:
                    data_df = data_df.drop(data_df.index[[0, 1]]).apply(pd.to_numeric)
                except ValueError as e:
                    print(e.args)
                    DataHeaderWarning(msg='SIMBA WARNING: SimBA found more than the expected two header column rows. SimBA will try to proceed '
                    'by removing one additional column header level. This can happen when you import multi-animal DLC data as standard DLC data.')
                    data_df = data_df.drop(data_df.index[[0, 1, 2]]).apply(pd.to_numeric).reset_index(drop=True)
            if 'scorer' in data_df.columns:
                data_df = data_df.set_index('scorer')
            data_df = insert_column_headers_for_outlier_correction(data_df=data_df, new_headers=self.header_line, filepath=file_path)
            data_df.index.name = None
            save_path = os.path.join(self.out_dir, video_name + '.' + self.file_type)
            save_df(data_df, self.file_type, save_path)
            self.file_cnt += 1
            print('Skipped outlier correction for video {} ...'.format(video_name))
        stdout_success(msg=f'Skipped outlier correction for {str(self.file_cnt)} files')

# test = OutlierCorrectionSkipper(config_path='/Users/simon/Desktop/troubleshooting/Zebrafish/project_folder/project_config.ini')
# test.skip_outlier_correction()

# test = OutlierCorrectionSkipper(config_path=r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Parquet_test2\project_folder\project_config.ini")
# test.skip_outlier_correction()

# test = OutlierCorrectionSkipper(config_path='/Users/simon/Desktop/troubleshooting/User_def_2/project_folder/project_config.ini')
# test.skip_outlier_correction()

# config_ini = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Parquet_test2\project_folder\project_config.ini"
# skip_outlier_c(config_ini)