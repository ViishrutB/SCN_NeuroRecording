from tarfile import data_filter
from traceback import print_tb
import pandas as pd
import numpy as np
import os
import scipy.io
from pandas import concat
from tabulate import tabulate as tb

# Reading Columns of CSV/XLSX Files
def read_columns(files):
    """Reads columns of XLSX/CSV files when supplied with a files"""
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
    """ Reads files in the folder when supplied with a folder_path"""
    file_list = []
    file_data = pd.DataFrame()

    for files in os.listdir(folder_path):
        for filename in os.listdir(os.path.join(folder_path, files)):
            file_list.append(folder_path + "\\" + files + "\\" + filename)

    file_data = read_columns(file_list)

    return file_data

## Code Usage

folder_path = r"E:\GittisLab_NeuralData"
file_data = read_files(folder_path)