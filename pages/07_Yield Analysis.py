import streamlit as st
import plotly.express as px

st.title("📉 Yield Analysis")
st.write("Lot/Batch별 수율과 불량률을 분석합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]
all_cols = df.columns.tolist()

st.info(f"현재 데이터: {st.session_state['file_name']}")

st.subheader("컬럼 선택")

lot_col = st.selectbox("Lot / Batch 컬럼 선택", all_cols)

good_col = st.selectbox("양품 수 컬럼 선택", numeric_cols)
defect_col = st.selectbox("불량 수 컬럼 선택", numeric_cols)

df_yield = df.copy()

df_yield["total_count"] = df_yield[good_col] + df_yield[defect_col]
df_yield["yield_rate"] = df_yield[good_col] / df_yield["total_count"] * 100
df_yield["defect_rate"] = df_yield[defect_col] / df_yield["total_count"] * 100

st.subheader("Yield KPI")

c1, c2, c3, c4 = st.columns(4)

c1.metric("평균 Yield", f"{df_yield['yield_rate'].mean():.2f}%")
c2.metric("최저 Yield", f"{df_yield['yield_rate'].min():.2f}%")
c3.metric("최고 Yield", f"{df_yield['yield_rate'].max():.2f}%")
c4.metric("총 생산 수량", int(df_yield["total_count"].sum()))

st.subheader("Lot / Batch별 Yield Trend")

fig_yield = px.line(
    df_yield,
    x=lot_col,
    y="yield_rate",
    markers=True,
    title="Yield Rate by Lot / Batch"
)

st.plotly_chart(fig_yield, use_container_width=True)

st.subheader("Lot / Batch별 Defect Rate")

fig_defect = px.bar(
    df_yield,
    x=lot_col,
    y="defect_rate",
    title="Defect Rate by Lot / Batch"
)

st.plotly_chart(fig_defect, use_container_width=True)

st.subheader("Yield 분석 결과 데이터")

st.dataframe(
    df_yield[[lot_col, good_col, defect_col, "total_count", "yield_rate", "defect_rate"]],
    use_container_width=True
)

st.subheader("Pareto Analysis")

defect_type_col = st.selectbox(
    "불량 유형 컬럼 선택",
    ["선택 안 함"] + all_cols
)

if defect_type_col != "선택 안 함":
    pareto_df = (
        df.groupby(defect_type_col)[defect_col]
        .sum()
        .reset_index()
        .sort_values(by=defect_col, ascending=False)
    )

    pareto_df["cum_ratio"] = pareto_df[defect_col].cumsum() / pareto_df[defect_col].sum() * 100

    fig_pareto = px.bar(
        pareto_df,
        x=defect_type_col,
        y=defect_col,
        title="Defect Pareto Chart"
    )

    st.plotly_chart(fig_pareto, use_container_width=True)

    st.dataframe(pareto_df, use_container_width=True)