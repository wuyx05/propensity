"""Module for loading and preprocessing raw data"""

import pandas as pd

def load_raw_data(file_path: str) -> dict:
    """Load Excel data from specified sheets
    
    Args:
        file_path: Path to Excel file
    Returns:
        Dictionary of DataFrames with sheet names as keys
    """
    sheets = ['Soc_Dem', 'Products_ActBalance', 'Inflow_Outflow', 'Sales_Revenues']
    return pd.read_excel(file_path, sheet_name=sheets, engine='openpyxl')

def preprocess_data(data: dict) -> pd.DataFrame:
    """Clean and merge raw datasets
    
    Args:
        data: Dictionary of raw DataFrames
    Returns:
        Merged and preprocessed DataFrame
    """
    
    df_demo = data['Soc_Dem']
    df_act = data['Products_ActBalance']
    df_flow = data['Inflow_Outflow']
    df_tar_rev = data['Sales_Revenues']
    df = (
        df_demo
        .merge(df_act, how='left', on='Client')
        .merge(df_flow, how='left', on='Client')
        .merge(df_tar_rev, how='left', on='Client')
    )
    
    
    count_cols = list(df_act.columns[df_act.columns.str.startswith('Count')])
    amt_cols=list((df_act.columns[~df_act.columns.str.startswith('Count')].append(df_flow.columns)).drop('Client'))
    target_cols= df_tar_rev.columns
    target_cols = [x for x in target_cols if x not in ['Client']]
    
    # Handle missing values and negative values
    df['Sex'] = df['Sex'].fillna('Unknown')
    df[count_cols] = df[count_cols].fillna(0).clip(lower=0)
    df[amt_cols] = df[amt_cols].fillna(0).clip(lower=0)
    print('Data loaded.')
    return df