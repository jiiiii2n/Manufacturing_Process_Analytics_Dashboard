import pandas as pd


def calculate_individual_control_limits(series):
    series = pd.Series(series).dropna()

    mean = series.mean()
    std = series.std()

    ucl = mean + 3 * std
    lcl = mean - 3 * std

    return mean, ucl, lcl


def calculate_moving_range(series):
    series = pd.Series(series).dropna()
    mr = series.diff().abs()
    return mr


def check_out_of_control(series, ucl, lcl):
    series = pd.Series(series)
    return (series > ucl) | (series < lcl)