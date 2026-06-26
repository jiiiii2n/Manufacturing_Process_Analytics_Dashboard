def calculate_kpi(df):
    return {
        "row_count": len(df),
        "column_count": len(df.columns)
    }
