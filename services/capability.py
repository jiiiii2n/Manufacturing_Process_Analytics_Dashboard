def calculate_cp_cpk(series, usl, lsl):
    mean = series.mean()
    std = series.std()

    cp = (usl - lsl) / (6 * std)
    cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std))

    return cp, cpk
