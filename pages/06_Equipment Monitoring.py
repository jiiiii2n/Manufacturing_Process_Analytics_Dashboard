import streamlit as st
import plotly.graph_objects as go

from services.dashboard import calculate_sensor_summary


st.title("🏭 Equipment Monitoring")
st.write("설비 센서 데이터의 추이와 요약 통계를 확인합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]
all_cols = df.columns.tolist()

st.info(f"현재 데이터: {st.session_state['file_name']}")

if not numeric_cols:
    st.error("수치형 컬럼이 없어 설비 모니터링을 수행할 수 없습니다.")
    st.stop()

st.subheader("센서 컬럼 선택")

selected_sensors = st.multiselect(
    "모니터링할 센서 컬럼을 선택하세요.",
    numeric_cols,
    default=numeric_cols[:3]
)

if not selected_sensors:
    st.warning("하나 이상의 센서 컬럼을 선택하세요.")
    st.stop()

x_col = st.selectbox("X축 컬럼 선택", all_cols)

st.subheader("Sensor Trend Chart")

fig = go.Figure()

for col in selected_sensors:
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[col],
        mode="lines+markers",
        name=col
    ))

fig.update_layout(
    title="Equipment Sensor Trend",
    xaxis_title=x_col,
    yaxis_title="Sensor Value"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Sensor Summary Statistics")

summary = calculate_sensor_summary(df, selected_sensors)
st.dataframe(summary, use_container_width=True)

st.subheader("Sensor KPI")

cols = st.columns(len(selected_sensors))

for i, sensor in enumerate(selected_sensors):
    with cols[i]:
        st.metric(
            label=f"{sensor} 평균",
            value=round(df[sensor].mean(), 4)
        )

st.subheader("Raw Sensor Data")

with st.expander("선택한 센서 데이터 보기"):
    st.dataframe(df[[x_col] + selected_sensors], use_container_width=True)