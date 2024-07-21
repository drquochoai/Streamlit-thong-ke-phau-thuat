import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import io
from tabulate import tabulate
import datetime


# from pygwalker.api.streamlit import StreamlitRenderer

from urllib.error import URLError
import urllib.request
# # urllib.request.urlretrieve("https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx", "files.xlsx")
st.set_page_config(
    page_title="Thống kê PTTT Ngoại TM-LN",
    layout="wide"
)
# @st.cache_data
# Load the custom CSS file
st.markdown(
    """
    <style>
    * {font-size: 12px}
    </style>
    """,
    unsafe_allow_html=True,
)

# """ AI requset: df['NGAY'] in csv is a datetype with stringtype, write code to convert df['NGAY'] to:
# if df['NGAY'] type is date, assign new date: with month to day and day to month, keep year
# if df['NGAY'] type is string, usually "12/07/2024 9:00", assign new date that get first 2 charactor as day, charactor 4 and 5 is month, and 7 to 10 is year
#  """
def convert_date(date_str):
    if isinstance(date_str, datetime.date):
        # If the input is a date object, swap month and day
        return datetime.date(date_str.year, date_str.day, date_str.month)
    elif isinstance(date_str, str):
        # If the input is a string, extract day, month, and year
        day, month, year = int(date_str[:2]), int(date_str[3:5]), int(date_str[6:10])
        return datetime.date(year, month, day)
    else:
        return datetime.date(1999, 9, 9)

def get_UN_data():
    # Hàm load file online, khi published
    try:
        # AWS_BUCKET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=csv"
        LINK_PUBLIC_TO_WEB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx"
        # AWS_BUCKET_URL = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/Thang%206%20PTTT.xlsx"
        LINK_EDIT = "https://docs.google.com/spreadsheets/d/18k646SexxQPgnhO6R4s1XghRitHrp2yFqynWSK9GqK8/edit"
        with urllib.request.urlopen(LINK_PUBLIC_TO_WEB) as response:
            file_object_load_GG_SHEET_directed_to_variable = io.BytesIO(
                response.read())
        # with open("temp_file.xlsx", "wb") as f:
        #     f.write(html)

        # Load the Excel file using openpyxl
        wb = load_workbook(file_object_load_GG_SHEET_directed_to_variable)
        # List all sheet names
        sheet_names = wb.sheetnames
        print("Sheet names:")
        for sheet_name in sheet_names:
            print(f"- {sheet_name}")
        option_Sheet_thong_ke = st.selectbox(
            "Chọn sheet muốn thống kê:",
            wb.sheetnames)

        df = pd.read_excel(
            file_object_load_GG_SHEET_directed_to_variable, sheet_name=option_Sheet_thong_ke, engine='openpyxl')
        # inf_bao = st.warning("Dữ liệu đã được tải thành công.")
        inf_moLinkEdit = st.link_button("Mở trang dữ liệu", url=LINK_EDIT)
        # df['NGAY'] = df['NGAY'].astype(str)
        if 'SONHA' in df.columns:
            df['SONHA'] = df['SONHA'].astype(str)
        if 'SOCMND' in df.columns:
            df['SOCMND'] = df['SOCMND'].astype(str)
        if 'NGAYCAP' in df.columns:
            df['NGAYCAP'] = df['NGAYCAP'].astype(str)
        if 'NGAY' in df.columns:
            df['NGAY'] = df['NGAY'].apply(convert_date)
        if 'NGAYKT' in df.columns:
            df['NGAYKT'] = df['NGAYKT'].apply(convert_date)
        if 'NGAYRV' in df.columns:
            df['NGAYRV'] = df['NGAYRV'].apply(convert_date)
        if 'NGAYRUT' in df.columns:
            df['NGAYRUT'] = df['NGAYRUT'].apply(convert_date)
        if 'NGAYCATCHI' in df.columns:
            df['NGAYCATCHI'] = df['NGAYCATCHI'].apply(convert_date)
        return df.reset_index(drop=True)

        with urllib.request.urlopen(LINK_PUBLIC_TO_WEB) as f:
            html = f.read()
    except URLError as e:
        st.error(f"Lỗi load file từ google sheet: {e}")

    # Hàm load file từ local, khi debug

    uploaded_file = st.file_uploader("Tải file xlSX")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        inf_bao.empty()
        return df.set_index("ID")


try:
    df = get_UN_data()
    dsbacsikhoaNTMLN = ["1342 TS.BS Nguyễn Anh Dũng", "6489 ThS. BS Trần Thúc Khang",
                        "2670 ThS.BS.CKI Lê Thị Ngọc Hằng", "3663 ThS.BS Nguyễn Hồng Vinh",
                        "2638 BS.CKI Trần Quốc Hoài", "4091 BS.CKI Phạm Ngọc Minh Thủy", "4972 ThS.BS Phan Vũ Hồng Hải", "6176 BS.CKI Lê Chí Hiếu"]
    dsbacsikhoaNTMLN_filter = [
        bs for bs in dsbacsikhoaNTMLN if bs in df["HOTEN1"].unique().tolist()]
    danhSachBacSi = st.multiselect(
        "Chọn bác sĩ", df["HOTEN1"].unique().tolist(),
        dsbacsikhoaNTMLN_filter
    )
    if not danhSachBacSi:
        st.error("Chọn ít nhất 1 bác sĩ.")
    else:
        data_GOC_NTMLN = df.loc[df["HOTEN1"].isin(danhSachBacSi)]
        
        # data /= 1000000.0
        
        
        dulieu_baoCao = data_GOC_NTMLN[['MABN', 'HOTEN', 'NAMSINH', 'NGAY', 'TENPT', 'HOTEN1']].rename(columns={'MABN': 'PID', 'HOTEN': 'Tên BN', 'HOTEN1': 'PTV', 'NAMSINH': "Năm sinh", 'NGAY': "Ngày PT", 'TENPT': "Tên phẫu thuật"})
        dulieu_baoCao = dulieu_baoCao.sort_values("Ngày PT")
        # add column "STT" as the first column of dulieu_baoCao, start from 1,2,3... to end
        dulieu_baoCao.insert(0, "STT", range(1, len(dulieu_baoCao) + 1))
        # st.write(dulieu_baoCao)
        
        st.header("Tổng số PT/TT: " + str(dulieu_baoCao.shape[0]))
        
        html_table = tabulate(dulieu_baoCao.sort_values("Ngày PT").to_dict("records"),
                              tablefmt="html", headers="keys")
        st.markdown(f'{html_table}', unsafe_allow_html=True)
        
        
        # PT theo danh mục
        st.header("Tổng số PT/TT theo danh mục:")
        unique_TENPTDM = data_GOC_NTMLN['TENPTDM'].unique()
        newdf = pd.DataFrame({'Tên PT/TT': unique_TENPTDM, 'Số lượng': data_GOC_NTMLN.groupby(
            'TENPTDM').size()}).reset_index(drop=True)
        total = newdf['Số lượng'].sum()
        new_row = pd.DataFrame({'Tên PT/TT': ['Tổng số'], 'Số lượng': [total]})
        newdf = pd.concat([newdf, new_row], ignore_index=True)
        # st.write(newdf)
        # Generate an HTML table using tabulate
        html_table = tabulate(newdf.to_dict("records"),
                              tablefmt="html", headers="keys")
        
        # Modify the HTML to include a specific ID and style
        html_table = f"""
        <table id="dmpt">
        {html_table[6:]}
        <style>
        table#dmpt tr:last-child {{ font-weight: bold; }}  # Target specific table
        </style>
        </table>
        """


        st.markdown(f'{html_table}', unsafe_allow_html=True)


        # # # # PTTT theo bác sĩ
        st.header("Tổng số PT/TT theo bác sĩ:")
        unique_HOTEN1 = data_GOC_NTMLN['HOTEN1'].unique()
        newdf = pd.DataFrame({'PTV': unique_HOTEN1, 'Số lượng': data_GOC_NTMLN.groupby(
            'HOTEN1').size()}).reset_index(drop=True)

        sorted_df = newdf.sort_values('Số lượng', ascending=False)
        # Generate an HTML table using tabulate
        html_table = tabulate(sorted_df.to_dict(
            "records"), tablefmt="html", headers="keys")
        
        st.markdown(f'{html_table}', unsafe_allow_html=True)
        # st.bar_chart(sorted_df.set_index("PTV"))
        # f'{df.to_markdown()}'
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
        st.header("Bảng full dữ liệu:")
        st.write("### Danh sách bệnh nhân đã phẫu thuật", data_GOC_NTMLN)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
