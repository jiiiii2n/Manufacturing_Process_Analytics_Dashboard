import streamlit as st
import plotly.express as px

from services.anomaly import detect_anomaly


st.title("🤖 Anomaly Detection")
st.write("제조 공정 데이터에서 이상값을 탐지합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]

st.info(f"현재 데이터: {st.session_state['file_name']}")

if len(numeric_cols) < 1:
    st.error("수치형 컬럼이 없어 이상 탐지를 수행할 수 없습니다.")
    st.stop()

st.subheader("이상 탐지 컬럼 선택")

selected_cols = st.multiselect(
    "이상 탐지에 사용할 수치형 컬럼을 선택하세요.",
    numeric_cols,
    default=numeric_cols[:2]
)

if not selected_cols:
    st.warning("하나 이상의 컬럼을 선택하세요.")
    st.stop()

st.subheader("이상 탐지 실행")

contamination = st.slider(
    "이상치 비율 설정",
    min_value=0.01,
    max_value=0.20,
    value=0.05,
    step=0.01
)

if st.button("이상 탐지 실행"):
    result = detect_anomaly(df, selected_cols, contamination)

    df_result = df.copy()
    df_result["anomaly"] = result
    df_result["anomaly_label"] = df_result["anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    anomaly_count = (df_result["anomaly"] == -1).sum()
    normal_count = (df_result["anomaly"] == 1).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("전체 데이터 수", len(df_result))
    c2.metric("정상 데이터 수", normal_count)
    c3.metric("이상 데이터 수", anomaly_count)

    st.subheader("이상 탐지 결과")

    if len(selected_cols) >= 2:
        fig = px.scatter(
            df_result,
            x=selected_cols[0],
            y=selected_cols[1],
            color="anomaly_label",
            title="Anomaly Detection Result"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.scatter(
            df_result,
            x=df_result.index,
            y=selected_cols[0],
            color="anomaly_label",
            title="Anomaly Detection Result"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("이상 데이터 목록")
    anomaly_df = df_result[df_result["anomaly"] == -1]

    if len(anomaly_df) > 0:
        st.dataframe(anomaly_df, use_container_width=True)
    else:
        st.success("탐지된 이상 데이터가 없습니다.")

    st.subheader("전체 결과 데이터")
    with st.expander("전체 결과 보기"):
        st.dataframe(df_result, use_container_width=True)