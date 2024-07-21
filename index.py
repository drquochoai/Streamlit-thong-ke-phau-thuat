import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import io
from tabulate import tabulate
import datetime
import my_data_process_library as mylib

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


try:
    sheeturl = st.text_input(
        "Nhập link file excel", "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx")
    df = mylib.get_UN_data(sheeturl)

    # dsbacsikhoaNTMLN = ["1342 TS.BS Nguyễn Anh Dũng", "6489 ThS. BS Trần Thúc Khang",
    #                     "2670 ThS.BS.CKI Lê Thị Ngọc Hằng", "3663 ThS.BS Nguyễn Hồng Vinh",
    #                     "2638 BS.CKI Trần Quốc Hoài", "4091 BS.CKI Phạm Ngọc Minh Thủy", "4972 ThS.BS Phan Vũ Hồng Hải", "6176 BS.CKI Lê Chí Hiếu"]
    # dsbacsikhoaNTMLN_filter = [
    #     bs for bs in dsbacsikhoaNTMLN if bs in df["HOTEN1"].unique().tolist()]
    # # df["HOTEN1"].unique().tolist()
    keywords = ["Nguyễn Anh Dũng", "Trần Thúc Khang",
                        "Lê Thị Ngọc Hằng", "Nguyễn Hồng Vinh",
                        "Trần Quốc Hoài", "Phạm Ngọc Minh Thủy", "Phan Vũ Hồng Hải", "Lê Chí Hiếu", "Nguyễn Minh Trí Viên", "Bùi Trọng Đạt"]
    filtered_DanhSachBacSi = [name for name in df["HOTEN1"].unique().tolist() if any(keyword.lower() in name.lower() for keyword in keywords)] 
    # print(filtered_names)

    danhSachBacSi = st.multiselect(
        "Chọn bác sĩ", df["HOTEN1"].unique().tolist(),
        filtered_DanhSachBacSi
    )
    if not danhSachBacSi:
        st.error("Chọn ít nhất 1 bác sĩ.")
    else:
        data_GOC_NTMLN = df.loc[df["HOTEN1"].isin(danhSachBacSi)]

        # data /= 1000000.0

        dulieu_baoCao = data_GOC_NTMLN[['MABN', 'HOTEN', 'NAMSINH', 'NGAY', 'TENPT', 'HOTEN1']].rename(
            columns={'MABN': 'PID', 'HOTEN': 'Tên BN', 'HOTEN1': 'PTV', 'NAMSINH': "Năm sinh", 'NGAY': "Ngày PT", 'TENPT': "Tên phẫu thuật"})
        dulieu_baoCao = dulieu_baoCao.sort_values("Ngày PT")
        # add column "STT" as the first column of dulieu_baoCao, start from 1,2,3... to end
        dulieu_baoCao.insert(0, "STT", range(1, len(dulieu_baoCao) + 1))
        # st.write(dulieu_baoCao)

        st.header("Tổng số PT/TT: " + str(dulieu_baoCao.shape[0]))
        with st.expander("Danh sách bệnh nhân"):
            html_table = tabulate(dulieu_baoCao.sort_values("Ngày PT").to_dict("records"),
                                  tablefmt="html", headers="keys")
            st.markdown(f'{html_table}', unsafe_allow_html=True)

        # PT theo danh mục
        # st.header("Tổng số PT/TT theo danh mục:")
        unique_TENPTDM = data_GOC_NTMLN['TENPTDM'].unique()
        so_luong = data_GOC_NTMLN.groupby('TENPTDM').size().reindex(unique_TENPTDM, fill_value=0)  
        newdf = pd.DataFrame({'Tên PT/TT': unique_TENPTDM, 'Số lượng': so_luong}).reset_index(drop=True)
        total = newdf['Số lượng'].sum()
        new_row = pd.DataFrame({'Tên PT/TT': ['Tổng số'], 'Số lượng': [total]})
        newdf = pd.concat([newdf, new_row], ignore_index=True)
        # st.write(newdf)
        # Generate an HTML table using tabulate
        with st.expander("PT/TT theo danh mục:"):
            html_table = tabulate(newdf.to_dict("records"),
                                  tablefmt="html", headers="keys")
            html_table = f"""
            <table id="dmpt">
            {html_table[7:]}
            <style>
            table#dmpt tr:last-child {{ font-weight: bold; }}
            </style>
            </table>
            """
            st.markdown(f'{html_table}', unsafe_allow_html=True)

        # # # # PTTT theo bác sĩ
        st.header("Tổng số PT/TT theo bác sĩ:")
        unique_HOTEN1 = data_GOC_NTMLN['HOTEN1'].unique()
        so_luong = data_GOC_NTMLN.groupby('HOTEN1').size().reindex(unique_HOTEN1, fill_value=0)  
        newdf = pd.DataFrame({'PTV': unique_HOTEN1, 'Số lượng': so_luong}).reset_index(drop=True)

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
