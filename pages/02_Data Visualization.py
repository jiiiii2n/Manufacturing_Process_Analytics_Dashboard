import streamlit as st

from services.visualization import (
    make_line_chart,
    make_histogram,
    make_box_plot,
    make_scatter_plot,
    make_corr_heatmap
)

st.title("📈 Data Visualization")
st.write("업로드된 제조 공정 데이터를 시각화합니다.")

if "df" not in st.session_state:
    st.warning("먼저 Data Upload 페이지에서 데이터를 업로드하세요.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]
all_cols = df.columns.tolist()

st.info(f"현재 데이터: {st.session_state['file_name']}")

if not numeric_cols:
    st.error("수치형 컬럼이 없어 시각화할 수 없습니다.")
    st.stop()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Line Chart",
    "Histogram",
    "Box Plot",
    "Scatter Plot",
    "Correlation"
])

with tab1:
    x_col = st.selectbox("X축 컬럼 선택", all_cols, key="line_x")
    y_col = st.selectbox("Y축 컬럼 선택", numeric_cols, key="line_y")

    fig = make_line_chart(df, x_col, y_col)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    hist_col = st.selectbox("Histogram 컬럼 선택", numeric_cols, key="hist_col")

    fig = make_histogram(df, hist_col)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    box_col = st.selectbox("Box Plot 컬럼 선택", numeric_cols, key="box_col")

    fig = make_box_plot(df, box_col)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    scatter_x = st.selectbox("X축 선택", numeric_cols, key="scatter_x")
    scatter_y = st.selectbox("Y축 선택", numeric_cols, key="scatter_y")

    fig = make_scatter_plot(df, scatter_x, scatter_y)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    selected_cols = st.multiselect(
        "상관관계를 볼 컬럼 선택",
        numeric_cols,
        default=numeric_cols
    )

    if len(selected_cols) >= 2:
        fig = make_corr_heatmap(df, selected_cols)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("2개 이상의 수치형 컬럼을 선택하세요.")