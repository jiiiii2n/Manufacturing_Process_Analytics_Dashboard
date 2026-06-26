import pandas as pd


def get_column_info(df):
    return pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str),
        "missing_count": df.isnull().sum().values,
        "missing_ratio(%)": (df.isnull().sum().values / len(df) * 100).round(2),
        "unique_count": df.nunique().values
    })


def check_missing_values(df):
    return df.isnull().sum()