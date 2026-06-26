from sklearn.ensemble import IsolationForest


def detect_anomaly(df, cols, contamination=0.05):
    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    result = model.fit_predict(df[cols])
    return result