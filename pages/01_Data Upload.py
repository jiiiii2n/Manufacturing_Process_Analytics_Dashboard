import streamlit as st

from services.data_loader import load_data
from services.preprocessing import get_column_info, check_missing_values
from utils.helper import get_numeric_columns, get_datetime_columns


st.title("📂 Data Upload")
st.write("CSV / Excel 제조 공정 데이터를 업로드하고 기본 정보를 확인합니다.")

if "df" in st.session_state:
    st.info(f"현재 저장된 데이터: {st.session_state['file_name']}")

uploaded_file = st.file_uploader(
    "CSV 또는 Excel 파일을 업로드하세요.",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)

        st.session_state["df"] = df
        st.session_state["file_name"] = uploaded_file.name
        st.session_state["numeric_cols"] = get_numeric_columns(df)
        st.session_state["datetime_cols"] = get_datetime_columns(df)

        st.success("파일 업로드 완료 및 세션 저장 완료")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

if "df" in st.session_state:
    df = st.session_state["df"]

    st.subheader("1. 데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("2. 데이터 크기")
    col1, col2, col3 = st.columns(3)

    col1.metric("행 개수", df.shape[0])
    col2.metric("열 개수", df.shape[1])
    col3.metric("수치형 컬럼 수", len(st.session_state["numeric_cols"]))

    st.subheader("3. 컬럼 정보")
    st.dataframe(get_column_info(df), use_container_width=True)

    st.subheader("4. 결측치 확인")
    missing_values = check_missing_values(df)

    if missing_values.sum() == 0:
        st.success("결측치가 없습니다.")
    else:
        st.warning("결측치가 존재합니다.")
        st.dataframe(missing_values, use_container_width=True)

    st.subheader("5. 기본 통계량")
    numeric_cols = st.session_state["numeric_cols"]

    if numeric_cols:
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    else:
        st.info("수치형 컬럼이 없습니다.")

    if st.button("저장된 데이터 초기화"):
        st.session_state.clear()
        st.rerun()

else:
    st.info("CSV 또는 Excel 파일을 업로드하면 데이터 정보가 표시됩니다.")