def calculate_kpi(df):
    return {
        "row_count": len(df),
        "column_count": len(df.columns)
    }


def calculate_sensor_summary(df, selected_cols):
    summary = df[selected_cols].describe().T
    summary = summary[["mean", "std", "min", "max"]]
    return summary