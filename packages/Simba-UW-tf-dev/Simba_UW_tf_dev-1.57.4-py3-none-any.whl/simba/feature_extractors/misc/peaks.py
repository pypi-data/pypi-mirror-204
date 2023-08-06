import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import lilliefors
from scipy.signal import find_peaks


def rolling_frequentist_distribution_tests(data: np.array, name: str):
    rolling_idx = np.arange(50)[None, :] + 1*np.arange(data.shape[0])[:, None]
    ks_results, ttest_results = np.full((data.shape[0]), -1.0), np.full((data.shape[0]), -1.0)
    lillefors_results, shapiro_results = np.full((data.shape[0]), -1.0),  np.full((data.shape[0]), -1.0)
    peak_cnt_results = np.full((data.shape[0]), -1.0)
    for i in range(50, data.shape[0] - 50, 50):
        bin_1_idx, bin_2_idx = [i-50, i], [i, i+50]
        bin_1_data, bin_2_data = data[bin_1_idx[0]:bin_1_idx[1]], data[bin_2_idx[0]:bin_2_idx[1]]
        ks_results[i:i+51] = stats.ks_2samp(data1=bin_1_data, data2=bin_2_data).statistic
        ttest_results[i:i+51] = stats.ttest_ind(bin_1_data, bin_2_data).statistic
    for i in range(0, data.shape[0]-50, 50):
        lillefors_results[i:i+51] = lilliefors(data[i:i+50])[0]
        shapiro_results[i:i+51] = stats.shapiro(data[i:i+50])[0]
    for i in range(rolling_idx.shape[0]):
        bin_start_idx, bin_end_idx = rolling_idx[i][0], rolling_idx[i][-1]
        peaks, _ = find_peaks(data[bin_start_idx:bin_end_idx], height=0)
        peak_cnt_results[i] = len(peaks)

    columns = [f'{name}_KS', f'{name}_TTEST', f'{name}_LILLEFORS', f'{name}_SHAPIRO', f'{name}_PEAK_CNT']
    return pd.DataFrame(np.column_stack((ks_results, ttest_results,
                                        lillefors_results, shapiro_results, peak_cnt_results)), columns=columns)


features = [f'Convex_hull_mean_25_window']
DATA_PATH = '/Users/simon/Desktop/envs/troubleshooting/naresh/project_folder/csv/features_extracted/SF2.csv'
data = pd.read_csv(DATA_PATH, index_col=0)
for feature in features:
    df = rolling_frequentist_distribution_tests(data=data[feature].astype(int).values, name=feature)
    print(df)


