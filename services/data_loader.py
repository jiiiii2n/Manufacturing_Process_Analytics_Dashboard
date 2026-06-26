import pandas as pd


def load_data(uploaded_file):
    file_name = uploaded_file.name
    file_ext = file_name.split(".")[-1].lower()

    if file_ext == "csv":
        return pd.read_csv(uploaded_file)

    elif file_ext in ["xlsx", "xls"]:
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")