#Description: This is a stock market dashboard to show some charts and data on some stock

#Import the libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#Add a title
st.title('Stock Web')

#Load the data
vn30_url = ("https://raw.githubusercontent.com/ThuPhuong2042/project/main/vn30.csv")
vn30 = pd.read_csv(vn30_url)

#Von hoa
vnshort = vn30[['MACOPHIEU', 'GIADONGCUA', 'KLGD', 'VONHOA ', 'THAYDOI']].copy()
conditions = [(vnshort['THAYDOI'] > 0), (vnshort['THAYDOI'] < 0), (vnshort['THAYDOI'] == 0)]
values = ['Tăng giá', 'Giảm giá', 'Đứng giá']
vnshort['Biến động'] = np.select(conditions, values)
area = vnshort['VONHOA ']
vonhoa = px.scatter(vnshort, x='GIADONGCUA', y='KLGD',
                 size=area,color ='Biến động',
                 color_discrete_sequence=["green", "red","yellow"],
                 hover_name = 'MACOPHIEU')
vonhoa.update_layout(title='Biểu đồ vốn hoá')

#Do rong
vn30['THAYDOIDAUPHIEN']=vn30['GIAMOCUA']-vn30['GIATHAMCHIEU']
data={'Time':['9:16','15:00']}
data=pd.DataFrame(data, columns=['Time','Tang','Giam','DungGia'])
data=data.fillna(0)
for i in range(len(vn30)):
    if vn30['THAYDOIDAUPHIEN'][i]<0:
        data.iloc[0,2]+=1
    elif vn30['THAYDOIDAUPHIEN'][i]==0:
        data.iloc[0,3]+=1
    else:
        data.iloc[0,1]+=1
for i in range(len(vn30)):
    if vn30.iloc[i,11]<0:
        data.iloc[1,2]+=1
    elif vn30.iloc[i,11]==0:
        data.iloc[1,3]+=1
    else:
        data.iloc[1,1]+=1

datas = data[['Tang','Giam','DungGia']]
data_perc = datas.divide(data.sum(axis=1), axis= 0)
data_perc['Time']=data.Time

fig = go.Figure()
fig = fig.add_trace(go.Scatter(
x=data_perc.Time, y=data_perc.Giam,
hoverinfo='x+y',fillcolor='firebrick',line_color="firebrick",
mode='lines',name = 'Giảm giá',
stackgroup='one'))
fig = fig.add_trace(go.Scatter(
x=data_perc.Time, y = data_perc.DungGia,
hoverinfo='x+y', fillcolor='gold',line_color='gold',
mode='lines',name = 'Đứng giá',
stackgroup = 'one'))
fig = fig.add_trace(go.Scatter(
x=data_perc.Time, y = data_perc.Tang,
hoverinfo='x+y',fillcolor='limegreen',line_color="limegreen",
mode='lines',name = 'Tăng giá',
stackgroup='one'))
fig = fig.update_layout(title_text='Độ rộng thị trường',yaxis_range=(0, 1))

#Dan dat thi truong
df_url =('https://raw.githubusercontent.com/ThuPhuong2042/project/main/Data_VN30.csv')
df = pd.read_csv(df_url)
KLNIEMYET_GIATHAMCHIEU = df["GIATHAMCHIEU"] * df["KLNIEMYET"]
KLNIEMYET_GIAKHOP = df["GIADONGCUA"] * df["KLNIEMYET"]
VNI = 1- (KLNIEMYET_GIATHAMCHIEU.sum())/(KLNIEMYET_GIAKHOP.sum())
index_return = df["THAYDOI"]
# Select the market capitalization
market_cap = df["VONHOA"]
# Calculate the total market cap
total_market_cap = df["VONHOA"].sum()
# Calculate the component weights
weights =  market_cap/total_market_cap
# Calculate and plot the contribution by component
df["DIEMANHHUONG"] = weights * index_return
mask = df['DIEMANHHUONG'] < 0
df['DIEMANHHUONGDUONG'] = df['DIEMANHHUONG'].mask(mask)
df['DIEMANHHUONGAM'] = df['DIEMANHHUONG'].mask(~mask)
df1 = df.sort_values(by = ['DIEMANHHUONGDUONG','DIEMANHHUONGAM'], ascending = [False, False])
df = pd.concat([df, df1], axis=1)
df2 = df1[['DIEMANHHUONGDUONG','DIEMANHHUONGAM','MACOPHIEU']]
df2 = df1[['DIEMANHHUONGDUONG','DIEMANHHUONGAM','MACOPHIEU']]
df2 = df2.set_index('MACOPHIEU')
topduong = df2.nlargest(10, 'DIEMANHHUONGDUONG')
topam = df2.nsmallest(10, 'DIEMANHHUONGAM')
d = (topduong["DIEMANHHUONGDUONG"].reset_index()).set_index('MACOPHIEU')
a = (topam["DIEMANHHUONGAM"].sort_values(ascending=False).reset_index()).set_index('MACOPHIEU')
df3 = pd.concat([d, a])
fig1 = go.Figure()
fig1 = fig1.add_trace(go.Bar(x=df3.index, y=df3['DIEMANHHUONGDUONG'],
                             name = 'Điểm ảnh hưởng dương',marker={'color':'green'},width=0.8))
fig1 = fig1.add_trace(go.Bar(x=df3.index, y=df3['DIEMANHHUONGAM'],
                             name = 'Điểm ảnh hưởng âm',marker={'color':'red'},width=0.8))
fig1.update_layout(title_text='Nhóm dẫn dắt thị trường')


#Display
status = st.sidebar.selectbox("Tổng quan thị trường",
                      ['Nhóm dẫn dắt thị trường','Độ rộng thị trường','Biểu đồ vốn hoá'])
if (status == 'Biểu đồ vốn hoá' ):
    st.plotly_chart(vonhoa)
elif (status == 'Độ rộng thị trường'):
    st.plotly_chart(fig)
else:
    st.plotly_chart(fig1)

