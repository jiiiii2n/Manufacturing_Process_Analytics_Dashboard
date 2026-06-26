from sklearn.ensemble import IsolationForest

def detect_anomaly(df, cols):
    model = IsolationForest(contamination=0.05, random_state=42)
    result = model.fit_predict(df[cols])
    return result
