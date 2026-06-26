import streamlit as st
import plotly.graph_objects as go

from services.capability import (
    calculate_cp_cpk,
    calculate_pp_ppk,
    capability_judgement
)


st.title("📐 Process Capability")
st.write("USL/LSL 기준으로 공정능력지수 Cp, Cpk, Pp, Ppk를 계산합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]

st.info(f"현재 데이터: {st.session_state['file_name']}")

if not numeric_cols:
    st.error("수치형 컬럼이 없어 공정능력 분석을 수행할 수 없습니다.")
    st.stop()

target_col = st.selectbox("공정능력 분석 대상 컬럼 선택", numeric_cols)

series = df[target_col].dropna()

default_mean = float(series.mean())
default_std = float(series.std())

st.subheader("Spec Limit 입력")

col1, col2 = st.columns(2)

with col1:
    lsl = st.number_input(
        "LSL",
        value=float(default_mean - 3 * default_std)
    )

with col2:
    usl = st.number_input(
        "USL",
        value=float(default_mean + 3 * default_std)
    )

if usl <= lsl:
    st.error("USL은 LSL보다 커야 합니다.")
    st.stop()

result_cp = calculate_cp_cpk(series, usl, lsl)
result_pp = calculate_pp_ppk(series, usl, lsl)

judgement = capability_judgement(result_cp["cpk"])

st.subheader("공정능력 결과")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cp", round(result_cp["cp"], 4))
c2.metric("Cpk", round(result_cp["cpk"], 4))
c3.metric("Pp", round(result_pp["pp"], 4))
c4.metric("Ppk", round(result_pp["ppk"], 4))

st.subheader("공정능력 판정")

if judgement == "Excellent":
    st.success(f"판정: {judgement}")
elif judgement == "Good":
    st.info(f"판정: {judgement}")
elif judgement == "Marginal":
    st.warning(f"판정: {judgement}")
else:
    st.error(f"판정: {judgement}")

st.subheader("상세 통계")

detail = {
    "Mean": result_cp["mean"],
    "Std": result_cp["std"],
    "USL": usl,
    "LSL": lsl,
    "CPU": result_cp["cpu"],
    "CPL": result_cp["cpl"],
    "PPU": result_pp["ppu"],
    "PPL": result_pp["ppl"]
}

st.dataframe(detail, use_container_width=True)

st.subheader("Histogram with Spec Limits")

fig = go.Figure()

fig.add_trace(go.Histogram(
    x=series,
    nbinsx=30,
    name=target_col
))

fig.add_vline(
    x=lsl,
    line_dash="dash",
    annotation_text="LSL"
)

fig.add_vline(
    x=usl,
    line_dash="dash",
    annotation_text="USL"
)

fig.add_vline(
    x=result_cp["mean"],
    line_dash="dot",
    annotation_text="Mean"
)

fig.update_layout(
    title=f"{target_col} Capability Histogram",
    xaxis_title=target_col,
    yaxis_title="Count"
)

st.plotly_chart(fig, use_container_width=True)