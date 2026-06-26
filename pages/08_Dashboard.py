import streamlit as st
import plotly.express as px

st.title("📋 Manufacturing Dashboard")
st.write("업로드된 제조 공정 데이터의 핵심 지표를 요약합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]

st.info(f"현재 데이터: {st.session_state['file_name']}")

st.subheader("기본 KPI")

c1, c2, c3, c4 = st.columns(4)

c1.metric("데이터 행 수", df.shape[0])
c2.metric("데이터 열 수", df.shape[1])
c3.metric("수치형 컬럼 수", len(numeric_cols))
c4.metric("결측치 수", int(df.isnull().sum().sum()))

if not numeric_cols:
    st.error("수치형 컬럼이 없어 대시보드를 구성할 수 없습니다.")
    st.stop()

st.subheader("주요 공정 지표")

target_col = st.selectbox("대표 공정 지표 선택", numeric_cols)

mean_val = df[target_col].mean()
std_val = df[target_col].std()
max_val = df[target_col].max()
min_val = df[target_col].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric("평균", round(mean_val, 4))
c2.metric("표준편차", round(std_val, 4))
c3.metric("최댓값", round(max_val, 4))
c4.metric("최솟값", round(min_val, 4))

st.subheader("Trend Chart")

x_col = st.selectbox("X축 컬럼 선택", df.columns.tolist())

fig = px.line(
    df,
    x=x_col,
    y=target_col,
    markers=True,
    title=f"{target_col} Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("이상 신호 요약")

ucl = mean_val + 3 * std_val
lcl = mean_val - 3 * std_val

alarm_df = df[(df[target_col] > ucl) | (df[target_col] < lcl)]

c1, c2, c3 = st.columns(3)

c1.metric("UCL", round(ucl, 4))
c2.metric("LCL", round(lcl, 4))
c3.metric("관리한계 초과 수", len(alarm_df))

if len(alarm_df) > 0:
    st.warning("관리한계를 초과한 데이터가 존재합니다.")
    st.dataframe(alarm_df, use_container_width=True)
else:
    st.success("관리한계를 초과한 데이터가 없습니다.")

st.subheader("상관관계 요약")

if len(numeric_cols) >= 2:
    corr = df[numeric_cols].corr()

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("상관관계를 계산하려면 수치형 컬럼이 2개 이상 필요합니다.")