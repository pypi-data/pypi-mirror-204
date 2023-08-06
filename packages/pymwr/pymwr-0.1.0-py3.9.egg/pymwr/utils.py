import pandas as pd
import datetime
import numpy as np


def get_dates(mwr_data: pd.DataFrame) -> dict:
    """
    Extracts the starting dates of each file in a Level 2 MWR dataset.

    Parameters:
    -----------
    mwr_data: pd.DataFrame
        A Pandas DataFrame containing the Level 2 MWR data.

    Returns:
    --------
    dict
        A dictionary containing a list of starting dates for each file in the dataset.
    """
    data_records = mwr_data[mwr_data.eq('Record').any(axis=1)]
    col_400 = data_records[data_records.eq('400').any(axis=1)].drop_duplicates().values[0]
    data_dates = mwr_data.loc[data_records[data_records.eq('400').any(axis=1)].index+1]
    data_dates.columns = col_400
    return {'Each file starting date': list(data_dates['Date/Time'].values)}


def get_site_coords(mwr_data):
    """
    Extracts the latitude and longitude from microwave radiometer data.

    Parameters:
    -----------
    mwr_data : pandas DataFrame
        A pandas DataFrame containing microwave radiometer data.

    Returns:
    --------
    dict
        A dictionary containing the extracted latitude and longitude.

    Raises:
    -------
    None
    """
    data_records = mwr_data[mwr_data.eq('Record').any(axis=1)]
    col_pos = list(data_records[data_records.eq('Latitude').any(axis=1)].values[0])
    temp_df = mwr_data[mwr_data.eq('31').any(axis=1)]
    temp_df.columns = col_pos
    latitude, longitude = temp_df[['Latitude', 'Longitude']].drop_duplicates().astype(float).values[0]
    return {'Latitude': latitude, 'Longitude': longitude}


def get_height_levels(mwr_data: pd.DataFrame) -> dict:
    """
    Extracts the height levels of the MWR measurements in a Level 2 MWR dataset.

    Parameters:
    -----------
    mwr_data: pd.DataFrame
        A Pandas DataFrame containing the Level 2 MWR data.

    Returns:
    --------
    dict
        A dictionary containing a list of height levels (in km) for the MWR measurements.
    """
    data_records = mwr_data[mwr_data.eq('Record').any(axis=1)]
    temp = list(data_records[data_records.eq('LV2 Processor').any(axis=1)].values[0])
    mwr_ht = []
    for i in temp:
        try:
            mwr_ht.append(float(i))
        except ValueError:
            pass
    mwr_ht = mwr_ht[mwr_ht.index(0):]
    return {'MWR height levels (km)': mwr_ht}


def get_scan_data(mwr_data: pd.DataFrame, scan_angle: int, scan_code: int, quality_flag: str = '1') -> pd.DataFrame:
    """
    Extracts MWR profile data for a specific scan angle and scan code from a Level 2 MWR dataset.

    Parameters:
    -----------
    mwr_data: pd.DataFrame
        A Pandas DataFrame containing the Level 2 MWR data.
    scan_angle: int
        The scan angle to extract data for.
    scan_code: int
        The scan code to extract data for.
    quality_flag: str (default '1')
        The data quality flag to use for filtering.

    Returns:
    --------
    pd.DataFrame
        A Pandas DataFrame containing the MWR profile data for the specified scan angle and scan code.
    """
    data_records = mwr_data[mwr_data.eq('Record').any(axis=1)]
    col_lv2processor = list(data_records[data_records.eq('LV2 Processor').any(axis=1)].values[0])
    temp_df = mwr_data.copy()
    temp_df.columns = col_lv2processor
    profile_data = temp_df[(temp_df['400'] == str(scan_angle)) & (temp_df['LV2 Processor'] == str(scan_code))]
    profile_data['Date'] = pd.to_datetime(profile_data['Date/Time'])
    profile_data = profile_data[profile_data['DataQuality'] == quality_flag]
    profile_data = profile_data.drop(['Date/Time'], axis=1)
    return profile_data


def get_gaps(df):
    """Identify data gaps greater than or equal to 15 minutes
    df: pandas.DataFrame - DataFrame containing the data

    Returns
    -------
    pandas.DataFrame - DataFrame containing the original data plus any added rows to fill the gaps.
    """
    mwr1 = df.dropna(axis=1).copy()
    x1 = []
    mwr1.reset_index(drop=True, inplace=True)
    for kk in range(len(mwr1)-1):
        if (mwr1['Date'][kk+1]-mwr1['Date'][kk]) >= datetime.timedelta(minutes=15):
            x1.append(mwr1['Date'][kk]+datetime.timedelta(seconds=1))
            x1.append(mwr1['Date'][kk+1]-datetime.timedelta(seconds=1))

    x2 = pd.DataFrame({'Date': x1})
    if len(x2) > 0:
        df2 = pd.concat([mwr1, x2])
        df2 = df2.sort_values(by='Date', ascending=True)
    else:
        df2 = mwr1.sort_values(by='Date', ascending=True)
    df2 = df2.set_index('Date')
    df2 = df2.drop(['Record', '400', 'LV2 Processor', 'DataQuality'], axis=1)
    df2 = df2.replace('', np.nan).dropna(axis=1)
    df2.columns = [float(i) for i in df2.columns]
    return df2
