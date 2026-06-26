import streamlit as st
import plotly.graph_objects as go

from services.spc import (
    calculate_individual_control_limits,
    calculate_moving_range,
    check_out_of_control
)

st.title("📊 SPC")
st.write("업로드된 제조 공정 데이터의 관리도를 생성합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]

st.info(f"현재 데이터: {st.session_state['file_name']}")

if not numeric_cols:
    st.error("수치형 컬럼이 없어 SPC 분석을 수행할 수 없습니다.")
    st.stop()

target_col = st.selectbox("SPC 분석 대상 컬럼 선택", numeric_cols)

series = df[target_col].dropna().reset_index(drop=True)

mean, ucl, lcl = calculate_individual_control_limits(series)
out_of_control = check_out_of_control(series, ucl, lcl)

st.subheader("관리 한계값")

col1, col2, col3 = st.columns(3)
col1.metric("Center Line", round(mean, 4))
col2.metric("UCL", round(ucl, 4))
col3.metric("LCL", round(lcl, 4))

st.subheader("Individual Control Chart")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=series.index,
    y=series,
    mode="lines+markers",
    name=target_col
))

fig.add_trace(go.Scatter(
    x=series.index,
    y=[mean] * len(series),
    mode="lines",
    name="CL"
))

fig.add_trace(go.Scatter(
    x=series.index,
    y=[ucl] * len(series),
    mode="lines",
    name="UCL"
))

fig.add_trace(go.Scatter(
    x=series.index,
    y=[lcl] * len(series),
    mode="lines",
    name="LCL"
))

if out_of_control.any():
    fig.add_trace(go.Scatter(
        x=series.index[out_of_control],
        y=series[out_of_control],
        mode="markers",
        name="Out of Control",
        marker=dict(size=10, symbol="x")
    ))

fig.update_layout(
    title=f"{target_col} Individual Control Chart",
    xaxis_title="Sample Index",
    yaxis_title=target_col
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Moving Range Chart")

mr = calculate_moving_range(series).dropna().reset_index(drop=True)
mr_mean, mr_ucl, mr_lcl = calculate_individual_control_limits(mr)

fig_mr = go.Figure()

fig_mr.add_trace(go.Scatter(
    x=mr.index,
    y=mr,
    mode="lines+markers",
    name="Moving Range"
))

fig_mr.add_trace(go.Scatter(
    x=mr.index,
    y=[mr_mean] * len(mr),
    mode="lines",
    name="MR CL"
))

fig_mr.add_trace(go.Scatter(
    x=mr.index,
    y=[mr_ucl] * len(mr),
    mode="lines",
    name="MR UCL"
))

fig_mr.update_layout(
    title=f"{target_col} Moving Range Chart",
    xaxis_title="Sample Index",
    yaxis_title="Moving Range"
)

st.plotly_chart(fig_mr, use_container_width=True)

st.subheader("이상점 요약")

st.write(f"관리 한계 초과 데이터 수: {out_of_control.sum()}개")

if out_of_control.any():
    st.dataframe(df.loc[out_of_control[out_of_control].index], use_container_width=True)
else:
    st.success("관리 한계를 초과한 데이터가 없습니다.")