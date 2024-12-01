from tarfile import data_filter
from traceback import print_tb
import pandas as pd
import numpy as np
import os
import scipy.io
from pandas import concat
from tabulate import tabulate as tb
import matplotlib.pyplot as plt

# Reading Columns of CSV/XLSX Files
def read_columns(files):
    df_combined = pd.DataFrame()
    for file in files:

        df = pd.read_csv(file)
        spk_cols = [col for col in df.columns if 'SPK' in col]
        df_selected = df[spk_cols].rename(columns={col: f"{file[3:-4]}_{col[-3:]}" for col in spk_cols})
        df_combined = pd.concat([df_combined, df_selected], ignore_index=True)
        print(file + ' Completed')

    return df

# Reading data from the folder structure
def read_files(folder_path):
    file_list = []
    file_data = pd.DataFrame()

    for files in os.listdir(folder_path):
        for filename in os.listdir(os.path.join(folder_path, files)):
            file_list.append(folder_path + "\\" + files + "\\" + filename)

    file_data = read_columns(file_list)

    return file_data

def forced_locomotion(AI03_ts, AI03_val, AI02_ts, AI02_val):
    # ... (similar preprocessing as in MATLAB)

    # Compute Smoothed Velocity
    movTime = AI03_val
    onset_sec = np.where(np.diff(movTime) == 1)[0] / 5000
    offset_sec = np.where(np.diff(movTime) == -1)[0] / 5000

    # ... (similar processing for AI02_val)

    # ... (plotting and other analysis steps, similar to MATLAB)

    # Calculate movement binary
    movbin = np.zeros_like(time_all)
    movind = np.where(vel_cms > 0.1)[0]
    movbin[movind] = 1

    onset_mov = np.where(np.diff(movbin) == 1)[0] / 20000
    offset_mov = np.where(np.diff(movbin) == -1)[0] / 20000

    return onset_mov, offset_mov

def plot_fr(ts, start, fin):
    prerate = []
    boutrate = []
    postrate = []

    for i in range(len(start)):
        pre_spikerate = ts[(ts > start[i] - 1) & (ts < start[i])]
        bout_spikerate = ts[(ts > start[i]) & (ts < fin[i])]
        post_spikerate = ts[(ts > fin[i]) & (ts < fin[i] + 1)]

        plt.figure(figsize=(10, 10))
        plt.subplot(7, 6, i + 1)  # Adjust subplot layout as needed
        plt.hist(pre_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1), alpha=0.5)
        plt.hist(bout_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1), alpha=0.5)
        plt.hist(post_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1), alpha=0.5)
        plt.ylim(0, 10)

        prerate.append(np.histogram(pre_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1))[0])
        boutrate.append(np.histogram(bout_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1))[0])
        postrate.append(np.histogram(post_spikerate, bins=np.arange(min(ts), max(ts) + 0.1, 0.1))[0])

        plt.show()  # To display each subplot individually

    return prerate, boutrate, postrate

## Code Usage

folder_path = r"E:\GittisLab_NeuralData"
file_data = read_files(folder_path)