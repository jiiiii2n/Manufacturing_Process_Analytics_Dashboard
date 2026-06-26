import pandas as pd


def calculate_cp_cpk(series, usl, lsl):
    series = pd.Series(series).dropna()

    mean = series.mean()
    std = series.std()

    cp = (usl - lsl) / (6 * std)
    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    cpk = min(cpu, cpl)

    return {
        "mean": mean,
        "std": std,
        "cp": cp,
        "cpu": cpu,
        "cpl": cpl,
        "cpk": cpk
    }


def calculate_pp_ppk(series, usl, lsl):
    series = pd.Series(series).dropna()

    mean = series.mean()
    std = series.std(ddof=0)

    pp = (usl - lsl) / (6 * std)
    ppu = (usl - mean) / (3 * std)
    ppl = (mean - lsl) / (3 * std)
    ppk = min(ppu, ppl)

    return {
        "pp": pp,
        "ppu": ppu,
        "ppl": ppl,
        "ppk": ppk
    }


def capability_judgement(cpk):
    if cpk >= 1.67:
        return "Excellent"
    elif cpk >= 1.33:
        return "Good"
    elif cpk >= 1.00:
        return "Marginal"
    else:
        return "Need Improvement"