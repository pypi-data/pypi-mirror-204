import pandas as pd
import csv
import glob


def read(data_dir: str) -> pd.DataFrame:
    """
    Read Level 2 MWR data from CSV files in a directory.

    Parameters:
    -----------
    data_dir: str
        Path to the directory containing MWR data CSV files.

    Returns:
    --------
    pd.DataFrame
        A Pandas DataFrame containing the MWR data from all CSV files in the directory.
    """
    mwr_files = glob.glob(data_dir + '/*.csv')
    mwr_data = []
    for filename in mwr_files:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                mwr_data.append(row)
    mwr_data = pd.DataFrame(mwr_data)
    return mwr_data
