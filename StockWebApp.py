#Description: This is a stock market dashboard to show some charts and data on some stock

#Import the libraries
import streamlit as st
from bs4 import BeautifulSoup
import csv
import urllib.request
from python_graphql_client import GraphqlClient
import requests, time
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


#Add a title
st.title('Stock Web')

#Load the data
# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://gateway-iboard.ssi.com.vn/graphql")

# Create the query string and variables required for the request.
query = """
    query stockRealtimes($exchange: String) {
  stockRealtimes(exchange: $exchange) {
    stockNo
    ceiling
    floor
    refPrice
    stockSymbol
    stockType
    exchange
    matchedPrice
    matchedVolume
    priceChange
    priceChangePercent
    highest
    avgPrice
    lowest
    nmTotalTradedQty
    best1Bid
    best1BidVol
    best2Bid
    best2BidVol
    best3Bid
    best3BidVol
    best4Bid
    best4BidVol
    best5Bid
    best5BidVol
    best6Bid
    best6BidVol
    best7Bid
    best7BidVol
    best8Bid
    best8BidVol
    best9Bid
    best9BidVol
    best10Bid
    best10BidVol
    best1Offer
    best1OfferVol
    best2Offer
    best2OfferVol
    best3Offer
    best3OfferVol
    best4Offer
    best4OfferVol
    best5Offer
    best5OfferVol
    best6Offer
    best6OfferVol
    best7Offer
    best7OfferVol
    best8Offer
    best8OfferVol
    best9Offer
    best9OfferVol
    best10Offer
    best10OfferVol
    buyForeignQtty
    buyForeignValue
    sellForeignQtty
    sellForeignValue
    caStatus
    tradingStatus
    currentBidQty
    currentOfferQty
    remainForeignQtty
    session
    __typename
  }
}

"""
variables = {"exchange": "hose"}

# Synchronous request
data = client.execute(query=query, variables=variables)
# print(data)  #=> {'data': {'stockRealtimes': {'stockNo': 'hose:21', 'stockSymbol': "AAA"}}}
# df = pd.DataFrame.from_dict(data['data']['stockRealtimes'])
# print(df)
# df.to_csv('test.csv', index=False)

header_list = []
raw_data = data['data']['stockRealtimes']

header_list.append('stockSymbol')
header_list.append('ceiling')
header_list.append('floor')
header_list.append('refPrice')
header_list.append('best3Bid')
header_list.append('best3BidVol')
header_list.append('best2Bid')
header_list.append('best2BidVol')
header_list.append('best1Bid')
header_list.append('best1BidVol')
header_list.append('matchedPrice')
header_list.append('matchedVolume')
header_list.append('priceChange')
header_list.append('priceChangePercent')
header_list.append('best1Offer')
header_list.append('best1OfferVol')
header_list.append('best2Offer')
header_list.append('best2OfferVol')
header_list.append('best3Offer')
header_list.append('best3OfferVol')
header_list.append('highest')
# header_list.append('avgPrice')
header_list.append('lowest')
header_list.append('nmTotalTradedQty')
header_list.append('buyForeignQtty')
header_list.append('sellForeignQtty')
header_list.append('remainForeignQtty')

data_file = open('ckhoan.csv', 'w', newline='')

# create the csv writer object
csv_writer = csv.writer(data_file)
col_Names = ["CK", "Tran", "San", "TC",
             "Giamua3", "KLmua3", "Giamua2", "KLmua2", "Giamua1", "KLmua1",
             "Giakhop", "Khoiluongkhoplenh", "Thaydoi", "Phantramthaydoi",
             "Giaban3", "KLban3", "Giaban2", "KLban2", "Giaban1", "KLban1"
                                                                  "Caonhat", "Thapnhat", "TongKL",
             "DTNNmua", "DTNNban", "DTNNdu"]

# for emp in data:
count = 0
list_of_Allcells = []
for j in range(0, len(raw_data)):
    data_list = []
    if count == 0:
        csv_writer.writerow(col_Names)

        count += 1
    for i in range(0, len(header_list)):
        r = raw_data[j][header_list[i]]
        if ('priceChange' in header_list[i]):
            if (r != ''):
                if (header_list[i] == 'priceChange'):
                    r = '{:.2f}'.format(float(r) / 1000)
                else:
                    r = '{:.1f}'.format(float(r))
        else:
            r = r
        if (type(r) == int or type(r) == float):
            # b = header_list[i]
            #  if ('priceChangePercent' in header_list[i]):
            #        r = r/100000
            if ('Vol' in header_list[i] or 'Qt' in header_list[i] or r == 0):
                r = r
            else:
                r = r / 1000
            a = str(r)
        elif r == None:
            a = str(0)
        else:
            a = r
        data_list.append(a)
    list_of_Allcells.append(data_list)

    # Writing data of CSV file
for item in list_of_Allcells:
    csv_writer.writerow(item)

data_file.close()

# Asynchronous request
# import asyncio

# data = asyncio.run(client.execute_async(query=query, variables=variables))
# print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

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
