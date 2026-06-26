def get_numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def get_datetime_columns(df):
    return df.select_dtypes(include="datetime").columns.tolist()