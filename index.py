import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import io
from tabulate import tabulate
import datetime
import my_data_process_library as mylib
import plotly.express as px
import plotly.graph_objects as go

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
# Giả sử bạn đã có DataFrame 'data_GOC_NTMLN' với các cột 'TENPTDM' và 'A2'


def classify_procedure(procedure_description):
    keywords = {
        "LN_PTNS": ["sinh thiết phổi", "soi màng phổi sinh thiết", "nội soi lồng ngực", "kén khí", "cắt kén", "sinh thiết màng phổi", "cắt phổi không", "nội soi cắt màng ngoài tim", "giao cảm ngực", "hạch giao cảm", "soi lồng ngực", "soi lồng ngực sinh thiết"],
        "LN_U trung thất": ["trung thất"],
        "LN_Tuyến giáp": ["tuyến giáp", "cắt tuyến giáp", "cắt tuyến giáp"],
        "LN_cắt thùy phổi": ["thùy phổi"],
        "MM_Suy tĩnh mạch": ["laser", "giãn tĩnh mạch", "Lazer", "Laser"],
        "MM_Catheter cảnh hầm": ["để lọc máu", "catheter tĩnh mạch", "chọc tĩnh mạch cảnh"],
        "MM_AVF": ["để chạy thận", "nối thông"],
        "MM_Bypass mạch máu": ["thiếu máu mạn tính", "tắc động mạch chi cấp tính", "nối tĩnh mạch lách", "động mạch đùi sâu", "tắc mạch máu các chi", "bắc cầu gần điều", "bắc cầu tĩnh mạch", "tắc động mạch chi bán", "khâu vết thương mạch máu"],
        "MM_Bypass hẹp-tắc-phình ĐMC": ["bắc cầu động mạch chủ ngực", "bắc cầu động mạch chủ với các động", "thay đoạn động mạch chủ bụng trên và dưới thận", "phồng động mạch chủ bụng"],
        "TT_MM_Chích xơ TM": ["Gây xơ tĩnh"],
        "LN_DLMP": ["ẫn lưu khí", "phổi liên tục", "lưu màng phổi", "dẫn lưu tối thiểu khoang", "dẫn lư­u khí"],
        "LN_mổ mở": ["bóc vỏ màng", "bóc màng phổi", "u máu", "u bã đậu", "u lành phần mềm", "chỉ thép", "cơ hoành", "định lồng ngực", "viêm màng ngoài tim", "điều trị gãy xương", "rút nẹp vít", "tháo nửa bàn", "tháo khớp", "rạch áp xe", "sinh thiết hạch cổ", "hạch cổ bảo", "vét hạch cổ", "Sinh thiết hạch", "mở ngực", "khí quản", "u phần mềm", "gỡ dính", "rò phần mềm", "vết thương mạch máu", "vết thương phần mềm", "u mạch máu", "nhiễm trùng vết mổ", "khâu đơn giản vết thương", "lưu màng tim qua đường", "dẫn lưu dịch khoang màng", "cầm máu do chảy máu", "mở cạnh cổ dẫn", "dẫn lưu khoang màng tim", "Mở khoang và giải phóng mạch", "Dẫn lưu màng ngoài tim", "PT dẫn lưu áp xe phổi", "hạch lao to vùng nách"],
        "MM_DSA_Stent graft ĐMC": ["stent Graft", "stent động mạch chủ"],
        "MM_động mạch cảnh": ["động mạch cảnh"],
        "TT_VAC": ["áp lực âm"],
        "TT_NLN": ["chụp cắt lớp vi tính", "bỏ tổ chức hoại tử", "lọc tổ chức hoại tử", "Rút sonde dẫn", "Gây dính màng phổi", "Rút buồng tiêm", "băng vết mổ", "Chọc hút dịch", "Chọc dò dịch", "hút khí màng", "TT_Chọc hút khí", "bóng đối xung động", "dẫn lưu áp xe tồn", "Chọc hút", "chỉ khâu da", "Chọc dịch màng ngoài", "Chọc tháo dịch màng", "thiết phần mềm bằng phương", "Chọc dò và dẫn lưu màng", "phân phúc mạc"],
        "TIM_CABG": ["mạch vành"],
        "TIM_TBS": ["điều trị hẹp đường ra", "thông liên nhĩ", "thông liên thất", "tim một tâm thất", "hẹp van động mạch phổi", "hồi lưu tĩnh mạch phổi", "Fallot", "kênh nhĩ thất", "Band động mạch phổi", "còn ống động mạch", "không có van động mạch phổi", "hẹp đường ra thất phải"],
        "TIM_thay van hai lá": ["thay van hai lá"],
        "TIM_sửa van hai lá": ["tạo hình van hai lá", "sửa van tim", "nội soi sửa van hai lá"],
        "TIM_sửa van ba lá": ["thay van ba lá đơn thuần"],
        "TIM_thay van ĐMC": ["van động mạch chủ"],
        "TIM_u nhầy": ["u nhầy tim"],
        "LN_PTNS_hạch giao cảm": ["giao cảm ngực", "hạch giao cảm"],
        "LN_PTNS_nuss": ["Nuss", "lõm ngực", "lõm lồng ngực"],
        "MM_DSA_Can thiệp nội mạch": ["Chụp, nong", "Chụp và can thiệp", "số hóa xóa nền", "nong động mạch ngoại", "nong cầu nối động", "Hybrid điều trị bệnh mạch máu"]
    }

    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            if keyword.lower() in procedure_description.lower():
                return category
    return ""  # Nếu không khớp với bất kỳ từ khóa nào


try:
    global sheeturl
    sheeturl = st.text_input(
        "Nhập link file excel", "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNpA9xv7ci1tGPdF1I-HwPdPWNvyryr5YNQvXOwxKRIWdOg5zPy-2xvXjrRoChqeb6QmwQX-qO4-uO/pub?output=xlsx")
    col1, col2, col3, col4 = st.columns(4)  # Equal width columns
    button24 = col1.button("2024")
    button23 = col2.button("2023")
    button22 = col3.button("2022")
    button21 = col4.button("2021")

    if button23:
        sheeturl = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/files/2023.xlsx"
    if button22:
        sheeturl = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/files/2022.xlsx"
    if button21:
        sheeturl = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/files/2021.xlsx"
    if button24:
        sheeturl = "https://github.com/drquochoai/Streamlit-thong-ke-phau-thuat/raw/main/files/2024.xlsx"

    df = mylib.get_UN_data(sheeturl)

    # dsbacsikhoaNTMLN = ["1342 TS.BS Nguyễn Anh Dũng", "6489 ThS. BS Trần Thúc Khang",
    #                     "2670 ThS.BS.CKI Lê Thị Ngọc Hằng", "3663 ThS.BS Nguyễn Hồng Vinh",
    #                     "2638 BS.CKI Trần Quốc Hoài", "4091 BS.CKI Phạm Ngọc Minh Thủy", "4972 ThS.BS Phan Vũ Hồng Hải", "6176 BS.CKI Lê Chí Hiếu"]
    # dsbacsikhoaNTMLN_filter = [
    #     bs for bs in dsbacsikhoaNTMLN if bs in df["HOTEN1"].unique().tolist()]
    # # df["HOTEN1"].unique().tolist()
    # keywords = ["Nguyễn Anh Dũng", "Trần Thúc Khang",
    #             "Lê Thị Ngọc Hằng", "Nguyễn Hồng Vinh",
    #             "Trần Quốc Hoài", "Phạm Ngọc Minh Thủy", "Phan Vũ Hồng Hải", "Lê Chí Hiếu", "Nguyễn Minh Trí Viên", "Bùi Trọng Đạt"]
    keywords = ["Nguyễn Anh Dũng",
                "Lê Thị Ngọc Hằng",
                "Trần Quốc Hoài", "Phan Vũ Hồng Hải", "Lê Chí Hiếu",
                "Trần Công Quyền"]
    filtered_DanhSachBacSi = [name for name in df["HOTEN1"].unique().tolist(
    ) if any(keyword.lower() in name.lower() for keyword in keywords)]
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
            # html_table = tabulate(dulieu_baoCao.sort_values("Ngày PT").to_dict("records"),
            #                       tablefmt="html", headers="keys")
            # st.markdown(f'{html_table}', unsafe_allow_html=True)
            st.dataframe(dulieu_baoCao)

        # PT theo danh mục
        # st.header("Tổng số PT/TT theo danh mục:")
        unique_TENPTDM = data_GOC_NTMLN['TENPTDM'].unique()
        so_luong = data_GOC_NTMLN.groupby(
            'TENPTDM').size().reindex(unique_TENPTDM, fill_value=0)
        newdf_loaiNhomPT = pd.DataFrame(
            {'Tên PT/TT': unique_TENPTDM, 'Số lượng': so_luong}).reset_index(drop=True)
        total = newdf_loaiNhomPT['Số lượng'].sum()
        newdf_loaiNhomPT['Phân loại'] = newdf_loaiNhomPT['Tên PT/TT'].astype(str).apply(classify_procedure)
        # create new column name "Nhóm PT" for newdf_loaiNhomPT, if column "Phân loại" start with "MM_" > "Mạch máu", if start with "LN_" > "Lồng ngực", if start with "TIM_" > "Tim", if start with "TT_" > "Thủ thuật khác"
        newdf_loaiNhomPT['Nhóm PT'] = newdf_loaiNhomPT['Phân loại'].apply(lambda x: "Mạch máu" if x.startswith("MM_") else "Lồng ngực" if x.startswith("LN_") else "Tim" if x.startswith("TIM_") else "Thủ thuật khác")
        
        new_row = pd.DataFrame({'Tên PT/TT': ['Tổng số'], 'Số lượng': [total], 'Phân loại': ["-"], 'Nhóm PT': ["-"]})

        newdf_loaiNhomPT = pd.concat([newdf_loaiNhomPT, new_row], ignore_index=True)
        # st.write(newdf)
        # Generate an HTML table using tabulate
        with st.expander("PT/TT theo danh mục:"):
            html_table = tabulate(newdf_loaiNhomPT.to_dict("records"),
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
        so_luong = data_GOC_NTMLN.groupby(
            'HOTEN1').size().reindex(unique_HOTEN1, fill_value=0)
        newdf_theoPTV = pd.DataFrame(
            {'PTV': unique_HOTEN1, 'Số lượng': so_luong}).reset_index(drop=True)

        sorted_df = newdf_theoPTV.sort_values('Số lượng', ascending=False)
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
        # st.header("Bảng full dữ liệu:")
        # st.write("### Danh sách bệnh nhân đã phẫu thuật", data_GOC_NTMLN)

        # PT theo tháng
        data_GOC_NTMLN['Tháng'] = pd.to_datetime(
            data_GOC_NTMLN['NGAY']).dt.month
        data_GOC_NTMLN['Năm'] = pd.to_datetime(data_GOC_NTMLN['NGAY']).dt.year
        monthly_count = data_GOC_NTMLN.groupby(['Năm', 'Tháng']).size().reset_index(name='Số lượng')
        st.header("Tổng số PT/TT theo tháng:")
        # st.dataframe(monthly_count)
        # st.bar_chart(monthly_count, x='Tháng', y='Số lượng', color='Năm')
        fig = px.bar(monthly_count, x='Tháng', y='Số lượng',
                     color='Số lượng', text='Số lượng')
        st.plotly_chart(fig)
        
        # Tạo nhóm lớn cho các phẫu thuật
        # Pie chart
        col1, col2 = st.columns([4,8])
        grouped_NhomPT_Lon = newdf_loaiNhomPT.groupby('Nhóm PT')['Số lượng'].sum().reset_index(name='Số lượng')
        grouped_NhomPT_Lon = grouped_NhomPT_Lon[grouped_NhomPT_Lon['Nhóm PT'] != "-"]
        col1.dataframe(grouped_NhomPT_Lon)
        fig_pie = px.pie(grouped_NhomPT_Lon, values='Số lượng', names='Nhóm PT', labels={'Số lượng': 'Số lượng'},  title='Tỉ lệ phân loại phẫu thuật')
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        col2.plotly_chart(fig_pie)
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
 
        Connection error: %s
    """
        % e.reason
    )
