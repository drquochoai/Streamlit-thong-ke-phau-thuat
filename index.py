import streamlit as st
import pandas as pd
import altair as alt
# from pygwalker.api.streamlit import StreamlitRenderer

from urllib.error import URLError
import urllib.request
# # urllib.request.urlretrieve("https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx", "files.xlsx")
st.set_page_config(
    page_title="Thống kê PTTT Ngoại TM-LN",
    layout="wide"
)
# @st.cache_data
def get_UN_data():
    # Hàm load file online, khi published
    try:
        # AWS_BUCKET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=csv"
        AWS_BUCKET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx"
        # AWS_BUCKET_URL = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/Thang%206%20PTTT.xlsx"
        with urllib.request.urlopen(AWS_BUCKET_URL) as f:
            html = f.read()
            df = pd.read_excel(html, sheet_name=0, engine='openpyxl')
            return df.set_index("MABN")
    except URLError as e:
        st.error(f"Lỗi load file từ google sheet: {e}")
        
        
    # Hàm load file từ local, khi debug
    
    uploaded_file = st.file_uploader("Tải file xlSX")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        return df.set_index("MABN")

try:
    df = get_UN_data()
    danhSachBacSi = st.multiselect(
        "Chọn bác sĩ", df["HOTEN1"].tolist(), ["2638 BS.CKI Trần Quốc Hoài", "1342 TS.BS Nguyễn Anh Dũng", "3663 ThS.BS Nguyễn Hồng Vinh", "2670 ThS.BS.CKI Lê Thị Ngọc Hằng", "6489 ThS. BS Trần Thúc Khang", "6176 BS.CKI Lê Chí Hiếu", "4972 ThS.BS Phan Vũ Hồng Hải", "4091 BS.CKI Phạm Ngọc Minh Thủy"]
    )
    if not danhSachBacSi:
        st.error("Chọn ít nhất 1 bác sĩ.")
    else:
        data = df.loc[df["HOTEN1"].isin(danhSachBacSi)]
        # data /= 1000000.0
        st.write("### Danh sách bệnh nhân đã phẫu thuật", data)

        # data = data.T.reset_index()
        # data = pd.melt(data, id_vars=["index"]).rename(
        #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        # )
        st.header("Tổng số PT/TT: "+ str( data.shape[0]))

        unique_TENPTDM = data['TENPTDM'].unique()
        newdf = pd.DataFrame({'TENPTDM_UNI': unique_TENPTDM, 'Count': data.groupby('TENPTDM').size()}).reset_index(drop=True)

        st.write(newdf)

        # chart = (
        #     alt.Chart(data)
        #     .mark_area(opacity=0.3)
        #     .encode(
        #         x="year:T",
        #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #         color="Region:N",
        #     )
        # )
        # st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

