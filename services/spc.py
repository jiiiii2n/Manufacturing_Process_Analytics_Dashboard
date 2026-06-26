def calculate_control_limits(series):
    mean = series.mean()
    std = series.std()
    ucl = mean + 3 * std
    lcl = mean - 3 * std
    return mean, ucl, lcl
