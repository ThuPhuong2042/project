#Description: This is a stock market dashboard to show some charts and data on some stock

#Import the libraries
import streamlit as streamlit
from bs4 import BeautifulSoup
import csv
import urllib.request
import requests, time
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime


#Load the data
outfile = open("ckhoan.csv","w", newline='',encoding='utf-8')
writer = csv.writer(outfile)

webUrl = urllib.request.urlopen('https://raw.githubusercontent.com/ThuPhuong2042/project/main/cao.html')
source_code = webUrl.read()

#query = pyquery(source_code)

soup = BeautifulSoup(source_code)
#table_tag = soup.find_all('table',{'class' : 'price table-scroll-table'})
table = soup.find('table',{'class' : 'price table-scroll-table'})
list_of_rows = []
for row in table.find_all('tr'):
    list_of_cells = []
    for cell in row.find_all(["th","td"]):
        text = cell.text
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)



col_Names=["CK", "Tran", "San", "TC",
           "Giamua3","KLmua3","Giamua2","KLmua2","Giamua1","KLmua1",
           "Giakhop","Khoiluongkhoplenh","Thaydoi","Phantramthaydoi",
           "Giaban3","KLban3","Giaban2","KLban2","Giaban1","KLban1"
           "Caonhat","Thapnhat","TongKL",
           "DTNNmua","DTNNban","DTNNdu"]
writer.writerow(col_Names)

df = pd.read_csv("ckhoan.csv",names=col_Names)
df.head()
for item in list_of_rows:
     writer.writerow(item)
     print(' '.join(item))
df = pd.read_csv("ckhoan.csv",names=col_Names)
df = df.drop(0)
c = 0
outfile = open('table.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
list_of_rows = []

col_names = ["ID", "CK", "ISIN", "FIGI", "TENDOANHNGHIEP", "KLĐANGKY_NIEMYET", "KLLUUHANH", "NGAYNIEMYET"]
writer.writerow(col_names)

for i in range(1, 14):
    url = 'https://www.hsx.vn/Modules/Listed/Web/SymbolList?pageFieldName1=Code&pageFieldValue1=&pageFieldOperator1=eq&pageFieldName2=Sectors&pageFieldValue2=&pageFieldOperator2=&pageFieldName3=Sector&pageFieldValue3=00000000-0000-0000-0000-000000000000&pageFieldOperator3=&pageFieldName4=StartWith&pageFieldValue4=&pageFieldOperator4=&pageCriteriaLength=4&_search=false&nd=' + str(
        time.time()) + '&rows=30&page=' + str(i) + '&sidx=id&sord=desc'
    r = requests.get(url)
    json_data = json.loads(r.text)
    list_of_Allcells = []

    for j in range(0, json_data['records']):
        list_of_cells = []
        text = json_data['rows'][j]['cell']
        for cell in text:
            list_of_cells.append(cell)
        list_of_Allcells.append(list_of_cells)
    for item in list_of_Allcells:
        writer.writerow(item)

outfile.close()
df1 = pd.read_csv("table.csv", names = col_names)
df1 = df1.drop(0).drop(columns=['ID', 'ISIN', "FIGI"])
hose = df1.merge(df)

#Convert
hose['Giakhop'] = hose['Giakhop'].astype(float)
hose['Thaydoi'] = hose['Thaydoi'].astype(float)
hose['KLLUUHANH'] = hose['KLLUUHANH'].apply(lambda x:float(x.replace('.','').replace(',','.')))

#VONHOA column
hose['VONHOA'] = hose['Giakhop']*hose['KLLUUHANH']

#Von hoa plot
vonhoa = hose[['CK','Giakhop','KLLUUHANH','Thaydoi','VONHOA']].copy()
vonhoa = vonhoa.dropna()
conditions = [(vonhoa['Thaydoi'] > 0), (vonhoa['Thaydoi'] < 0), (vonhoa['Thaydoi'] == 0)]
values = ['Tăng giá', 'Giảm giá', 'Đứng giá']
vonhoa['Biến động'] = np.select(conditions, values)
area = vonhoa['VONHOA']
vonhoaplot = px.scatter(vonhoa, x='Giakhop', y='KLLUUHANH',
                 size=area,color ='Biến động',
                 color_discrete_map ={'Tăng giá':'green','Giảm giá':'red','Đứng giá':'yellow'},
                 hover_name = 'CK')
vonhoaplot.update_layout(title='Vốn hoá',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right", x=1))

#Dan dat thi truong
hshort = hose[['CK','VONHOA',"Thaydoi"]].copy()
hshort['weights'] = hshort['VONHOA'].apply(lambda x:x/hshort['VONHOA'].sum())
hshort['DIEMANHHUONG'] = hshort["Thaydoi"]*hshort['weights']
mask = hshort['DIEMANHHUONG'] < 0
hshort['DIEMANHHUONGDUONG'] = hshort['DIEMANHHUONG'].mask(mask)
hshort['DIEMANHHUONGAM'] = hshort['DIEMANHHUONG'].mask(~mask)
hshort = hshort.set_index('CK')
topduong = hshort.nlargest(10, 'DIEMANHHUONGDUONG')
topam = hshort.nsmallest(10, 'DIEMANHHUONGAM')
d = (topduong["DIEMANHHUONGDUONG"].reset_index()).set_index('CK')
a = (topam["DIEMANHHUONGAM"].sort_values(ascending=False).reset_index()).set_index('CK')
dandat = pd.concat([d, a])
dandatplot = go.Figure()
dandatplot = dandatplot.add_trace(go.Bar(x=dandat.index, y=dandat['DIEMANHHUONGDUONG'],
                             name = 'Điểm ảnh hưởng dương',marker={'color':'green'},width=0.8))
dandatplot = dandatplot.add_trace(go.Bar(x=dandat.index, y=dandat['DIEMANHHUONGAM'],
                             name = 'Điểm ảnh hưởng âm',marker={'color':'red'},width=0.8))
dandatplot.update_layout(title_text='Nhóm dẫn dắt thị trường',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right", x=1))


#Load data khuyen nghi
stock = pd.read_csv('https://raw.githubusercontent.com/ThuPhuong2042/project/main/stock_file.csv')

for i in range(1,len(stock['Date'])) :
    stock_loop = stock['Date'][i]
    stock_Date =  datetime.datetime.strptime(stock_loop,'%Y-%m-%d')
    stock['Date'][i] = stock_Date.date()
stock['Date'] = pd.to_datetime(stock.Date)

stock = stock.sort_values(by='Date',ascending = True)
stock = stock.set_index('Date')
vni = pd.read_csv("https://raw.githubusercontent.com/ThuPhuong2042/project/main/vni_table.csv").drop(
    ['a', 'b', 'c', 'd'], axis=1).apply(lambda x: x.str.replace(',', '.'))
vni = vni.drop(0)
vni.head()
vni['VNI_Close'] = vni['VNI_Close'].astype(float)

for i in range(1, len(vni['Date'])):
    loop = vni['Date'][i]
    vni_Date = datetime.datetime.strptime(loop, '%d/%m/%Y')
    vni['Date'][i] = vni_Date.date()

vni['Date'] = pd.to_datetime(vni.Date)
vni = vni.sort_values(by='Date', ascending=True)
vni = vni.set_index('Date')

vni['Percent Change'] = vni['VNI_Close'].pct_change()

vni_return = (vni['Percent Change'] + 1).cumprod()[-1]
returns_multiples = []
m = 0
tic_stock = []
# ma  = ['AAA','AAM','AAT','VNM','DGW','SSI','MWG','GMD']
ma = ['AAA', 'AAM', 'AAT', 'ABS', 'ABT', 'ACB', 'ACC', 'ACL', 'ADG', 'ADS', 'AGG', 'AGM', 'AGR',
      'AMD', 'ANV', 'APC', 'APG', 'APH', 'ASG', 'ASM', 'ASP', 'AST', 'ATG', 'BBC', 'BCE', 'BCG',
      'BCM', 'BFC', 'BHN', 'BIC', 'BID', 'BKG', 'BMC', 'BMI', 'BMP', 'BRC', 'BSI', 'BTP', 'BTT',
      'BVH', 'BWE', 'C32', 'C47', 'CAV', 'CCI', 'CCL', 'CDC', 'CEE', 'CHP', 'CIG', 'CII', 'CKG',
      'CLC', 'CLG', 'CLL', 'CLW', 'CMG', 'CMV', 'CMX', 'CNG', 'COM', 'CRC', 'CRE', 'CSM', 'CSV',
      'CTD', 'CTF', 'CTG', 'CTI', 'CTS', 'CVT', 'D2D', 'DAG', 'DAH', 'DAT', 'DBC', 'DBD', 'DBT',
      'DC4', 'DCL', 'DCM', 'DGC', 'DGW', 'DHA', 'DHC', 'DHG', 'DHM', 'DIG', 'DLG', 'DMC', 'DPG',
      'DPM', 'DPR', 'DQC', 'DRC', 'DRH', 'DRL', 'DSN', 'DTA', 'DTL', 'DTT', 'DVP', 'DXG', 'DXV',
      'EIB', 'ELC', 'EMC', 'EVE', 'EVG', 'FCM', 'FCN', 'FDC', 'FIR', 'FIT', 'FLC', 'FMC', 'FPT',
      'FRT', 'FTM', 'FTS', 'GAB', 'GAS', 'GDT', 'GEG', 'GEX', 'GIL', 'GMC', 'GMD', 'GSP', 'GTA',
      'GTN', 'GVR', 'HAG', 'HAH', 'HAI', 'HAP', 'HAR', 'HAS', 'HAX', 'HBC', 'HCD', 'HCM', 'HDB',
      'HBC', 'HDG', 'HHP', 'HHS', 'HID', 'HII', 'HMC', 'HNG', 'HOT', 'HPG', 'HPX', 'HQC', 'HRC',
      'HSG', 'HSL', 'HT1', 'HTI', 'HTL', 'HTN', 'HTV', 'HU1', 'HU3', 'HUB', 'HVH', 'HVN', 'HVX',
      'IBC', 'ICT', 'IDI', 'IJC', 'ILB', 'IMP', 'ITA', 'ITC', 'ITD', 'JVC', 'KBC', 'KDC', 'KDH',
      'KHP', 'KMR', 'KOS', 'KPF', 'KSB', 'L10', 'LAF', 'LBM', 'LCG', 'LCM', 'LDG', 'LEC', 'LGC',
      'LGL', 'LHG', 'LIX', 'LM8', 'LPB', 'LSS', 'MBB', 'MCG', 'MCP', 'MDG', 'MHC', 'MIG', 'MSB',
      'MSH', 'MSN', 'MWG', 'NAF', 'NAV', 'NBB', 'NAV', 'NBB', 'NCT', 'NHA', 'NHH', 'NKG', 'NLG',
      'NNC', 'NSC', 'NT2', 'NTL', 'NVL', 'NVT', 'OCB', 'OGC', 'OGC', 'OPC', 'PAC', 'PAN', 'PC1',
      'PDN', 'PDR', 'PET', 'PGC', 'PGD', 'PGI', 'PHC', 'PHR', 'PIT', 'PJT', 'PLP', 'PLX', 'PME',
      'PLX', 'PME', 'PMG', 'PNC', 'PNJ', 'POM', 'POW', 'PPC', 'PSH', 'PTB', 'PTC', 'PTL', 'PVD',
      'PVT', 'PXI', 'PXS', 'PXT', 'QBS', 'QCG', 'RAL', 'RDP', 'REE', 'RIC', 'ROS', 'S4A', 'SAB',
      'SAM', 'SAV', 'SBA', 'SBT', 'SBV', 'SC5', 'SCD', 'SCR', 'SCS', 'SFC', 'SFG', 'SFI', 'SGN',
      'SGR', 'SGT', 'SHA', 'SHI', 'SHP', 'SII', 'SJD', 'SJF', 'SJS', 'SKG', 'SMA', 'SMB', 'SMC',
      'SPM', 'SRC', 'SRF', 'SSB', 'SSC', 'SSI', 'ST8', 'STB', 'STG', 'STK', 'SVC', 'SVD', 'SVI',
      'SVT', 'SZC', 'SZL', 'TAC', 'TBC', 'TCB', 'TCD', 'TCH', 'TCL', 'TCM', 'TCO', 'TCR', 'TCT',
      'TDC', 'TDG', 'TDH', 'TDM', 'TDP', 'TDW', 'TEG', 'TGG', 'THG', 'THI', 'TIP', 'TIX', 'TLD',
      'TLG', 'TLH', 'TMP', 'TMS', 'TMT', 'TN1', 'TNA', 'TNC', 'TNH', 'TNI', 'TNT', 'TPB', 'TPC',
      'TRA', 'TRC', 'TS4', 'TSC', 'TTA', 'TTB', 'TTE', 'TIF', 'TV2', 'TVB', 'TVS', 'TVT', 'TYA',
      'UDC', 'UIC', 'VAF', 'VCA', 'VCB', 'VCF', 'VCG', 'VCI', 'VDP', 'VDS', 'VFG', 'VGC', 'VHC',
      'VHM', 'VIB', 'VIC', 'VID', 'VIP', 'VIS', 'VIX', 'VJC', 'VMD', 'VND', 'VNE', 'VNG', 'VNL',
      'VNM', 'VNS', 'VOS', 'VPB', 'VPD', 'VPG', 'VPH', 'VPI', 'VPS', 'VRC', 'VRE', 'VSC', 'VSH',
      'VSI', 'VTB', 'VTO', 'YBM', 'YEG']
for i in range(0, len(ma)):
    #     Tic =''
    Tic = stock[stock["Ticker"] == ma[i]]
    m = len(Tic)
    tic_stock.append(Tic)
    #     print(m)
    Tic['Percent Change'] = Tic['Adj.Close'].pct_change()
    if m != 0:
        stock_return = (Tic['Percent Change'] + 1).cumprod()[-1]
        returns_multiple = round((stock_return / vni_return), 2)
    #     t.append(Tic)

    returns_multiples.append(returns_multiple)
#     returns_multiple = round((stock_return / vni_return), 2)
# stock_return
# for s in t:
#     if t['Percent Change'] == 'AAA':
#          stock_return = (t['Percent Change'] + 1).cumprod()[-1]
# stock_return

# stock_return
# returns_multiple
rs_df = pd.DataFrame(list(zip(ma, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]
rs_df = rs_df.sort_values(by='RS_Rating', ascending=False)
#List khuyen nghi
# Checking Minervini conditions of top 30% of stocks in given list
exportList = pd.DataFrame(
    columns=['MÃ CỔ PHIẾU', 'CHỈ SỐ RS', 'SMA50', 'SMA150', 'SMA200', 'ĐÁY 52 TUẦN', 'ĐỈNH 52 TUẦN'])
rs_stocks = rs_df['Ticker']
for st in rs_stocks:
    try:
        #         rs_sto = []
        #         for sto in stock:
        #             if sto["Ticker"] == st:
        #                 rs_sto.append(sto)
        df = stock[stock["Ticker"] == st]
        sma = [50, 150, 200]
        for x in sma:
            df["SMA_" + str(x)] = round(df['Adj.Close'].rolling(window=x).mean(), 2)

        # Storing required values
        currentClose = df["Adj.Close"][-1]
        Pre_Close = df["Adj.Close"][-2]
        currentOpen = df["Open"][-1]
        Volume = df["Volume"][-1]
        Pre_volume = df["Volume"][-2]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = round(min(df["Low"][-260:]), 2)
        high_of_52week = round(max(df["High"][-260:]), 2)
        RS_Rating = round(rs_df[rs_df['Ticker'] == st].RS_Rating.tolist()[0])

        try:
            moving_average_200_20 = df["SMA_200"][-20]
        except Exception:
            moving_average_200_20 = 0

        # Condition 1: Current Price > 150 SMA and > 200 SMA
        condition_1 = currentClose > moving_average_150 > moving_average_200

        # Condition 2: 150 SMA and > 200 SMA
        condition_2 = moving_average_150 > moving_average_200

        # Condition 3: 200 SMA trending up for at least 1 month
        condition_3 = moving_average_200 > moving_average_200_20

        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        condition_4 = moving_average_50 > moving_average_150 > moving_average_200

        # Condition 5: Current Price > 50 SMA
        condition_5 = currentClose > moving_average_50

        # Condition 6: Current Price is at least 30% above 52 week low
        condition_6 = currentClose >= (1.3 * low_of_52week)

        # Condition 7: Current Price is within 25% of 52 week high
        condition_7 = currentClose >= (.75 * high_of_52week)

        # Condition 8: Close price > Open Price
        condition_8 = currentClose > currentOpen

        # Condition 9 : Increase volume
        condition_9 = Volume > (3 * Pre_volume) and currentClose > Pre_Close

        #         If all conditions above are true, add stock to exportList
        if (
                condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7 and condition_8 and condition_9):
            exportList = exportList.append(
                {'MÃ CỔ PHIẾU': st, 'CHỈ SỐ RS': RS_Rating, 'SMA50': moving_average_50, 'SMA150': moving_average_150
                    , 'SMA200': moving_average_200, 'ĐÁY 52 TUẦN': low_of_52week, 'ĐỈNH 52 TUẦN': high_of_52week},
                ignore_index=True)
    except Exception as e:
        print(e)
        print(f"Could not gather data on {st}")
# currentClose
exportList = exportList.sort_values(by='CHỈ SỐ RS', ascending=False)
# writer = ExcelWriter("ScreenOutput.xlsx")
# exportList.to_excel(writer, "Sheet1")
# writer.save()




#List xu huong
exportList2 = pd.DataFrame(
    columns=['MÃ CỔ PHIẾU', 'GIÁ ĐÓNG CỬA', 'CHỈ SỐ RS', 'SMA50', 'SMA150', 'SMA200', 'ĐÁY 52 TUẦN', 'ĐỈNH 52 TUẦN'])
rs_stocks = rs_df['Ticker']
for st in rs_stocks:
    try:

        df = stock[stock["Ticker"] == st]
        sma = [50, 150, 200]
        for x in sma:
            df["SMA_" + str(x)] = round(df['Adj.Close'].rolling(window=x).mean(), 2)

        # Storing required values
        currentClose = df["Adj.Close"][-1]
        Pre_Close = df["Adj.Close"][-2]
        currentOpen = df["Open"][-1]
        Volume = df["Volume"][-1]
        Volumn_20_average = df["Volume"][-20:].mean()
        Pre_volume = df["Volume"][-2]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = round(min(df["Low"][-260:]), 2)
        high_of_52week = round(max(df["High"][-260:]), 2)
        RS_Rating = round(rs_df[rs_df['Ticker'] == st].RS_Rating.tolist()[0])

        try:
            moving_average_200_20 = df["SMA_200"][-20]
        except Exception:
            moving_average_200_20 = 0

        # Condition 1: Current Price > 150 SMA and > 200 SMA
        condition_1 = currentClose > moving_average_150 > moving_average_200

        # Condition 2: 150 SMA and > 200 SMA
        condition_2 = moving_average_150 > moving_average_200

        # Condition 3: 200 SMA trending up for at least 1 month
        condition_3 = moving_average_200 > moving_average_200_20

        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        condition_4 = moving_average_50 > moving_average_150 > moving_average_200

        # Condition 5: Current Price > 50 SMA
        condition_5 = currentClose > moving_average_50

        # Condition 6: Current Price is at least 30% above 52 week low
        condition_6 = currentClose >= (1.3 * low_of_52week)

        # Condition 7: Current Price is within 25% of 52 week high
        condition_7 = currentClose >= (.75 * high_of_52week)

        #         If all conditions above are true, add stock to exportList
        if (
                condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):
            exportList2 = exportList2.append(
                {'MÃ CỔ PHIẾU': st, 'GIÁ ĐÓNG CỬA': currentClose, 'CHỈ SỐ RS': RS_Rating, 'SMA50': moving_average_50,
                 'SMA150': moving_average_150
                    , 'SMA200': moving_average_200, 'ĐÁY 52 TUẦN': low_of_52week, 'ĐỈNH 52 TUẦN': high_of_52week},
                ignore_index=True)
    except Exception as e:
        print(e)
        print(f"Could not gather data on {st}")
# currentClose
exportList2 = exportList2.sort_values(by='CHỈ SỐ RS', ascending=False)


#Display
streamlit.set_page_config(page_title='Khuyến nghị giao dịch cổ phiếu',layout="wide")
streamlit.title('Khuyến nghị giao dịch cổ phiếu')
streamlit.markdown('<p style="font-size:25px">Tổng quan thị trường</p>', unsafe_allow_html=True)
col1, col2 = streamlit.beta_columns(2)
with col1:
    streamlit.plotly_chart(vonhoaplot)
    streamlit.markdown('<p style="font-size:25px">Danh sách cổ phiếu có xu hướng tăng</p>', unsafe_allow_html=True)
    streamlit.dataframe(exportList2.assign(hack='').set_index('hack'))
with col2:
    streamlit.plotly_chart(dandatplot)
    streamlit.markdown('<p style="font-size:25px">Danh sách cổ phiếu khuyến nghị mua hôm nay</p>', unsafe_allow_html=True)
    streamlit.dataframe(exportList.assign(hack='').set_index('hack'))





