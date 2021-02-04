#Description: This is a stock market dashboard to show some charts and data on some stock

#Import the libraries
import streamlit as st
from bs4 import BeautifulSoup
import csv
import urllib.request
import requests, time
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



#Load the data
outfile = open("ckhoan.csv","w", newline='',encoding='utf-8')
writer = csv.writer(outfile)

webUrl = urllib.request.urlopen('https://raw.githubusercontent.com/ThuPhuong2042/project/main/22.html')
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
vonhoaplot.update_layout(title='Biểu đồ vốn hoá')

#Do rong


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
dandatplot.update_layout(title_text='Nhóm dẫn dắt thị trường')

#Display
status = st.sidebar.selectbox("Tổng quan thị trường",
                      ['Nhóm dẫn dắt thị trường','Độ rộng thị trường','Biểu đồ vốn hoá'])
if (status == 'Biểu đồ vốn hoá' ):
    st.plotly_chart(vonhoaplot)
elif (status == 'Nhóm dẫn dắt thị trường'):
    st.plotly_chart(dandatplot)

