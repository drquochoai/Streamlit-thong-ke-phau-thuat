import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError


# @st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=csv"
    # AWS_BUCKET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?gid=0&single=true&output=csv"
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file is not None:
        # df = pd.read_csv(AWS_BUCKET_URL)
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')


        return df.set_index("HOTEN1")

try:
    df = get_UN_data()
    countries = st.multiselect(
        "Chọn bác sĩ", list(df.index), ["2638 BS.CKI Trần Quốc Hoài", "1342 TS.BS Nguyễn Anh Dũng", "3663 ThS.BS Nguyễn Hồng Vinh", "2670 ThS.BS.CKI Lê Thị Ngọc Hằng", "6489 ThS. BS Trần Thúc Khang", "6176 BS.CKI Lê Chí Hiếu", "4972 ThS.BS Phan Vũ Hồng Hải", "4091 BS.CKI Phạm Ngọc Minh Thủy"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        # data /= 1000000.0
        st.write("### Danh sách bệnh nhân đã phẫu thuật", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

