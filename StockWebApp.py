#Description: This is a stock market dashboard to show some charts and data on some stock

#Import the libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#Add a title
st.title('Stock Web')

#Load the data
vn30 = pd.read_csv("C:/Users/ThuPhuong/PycharmProjects/pythonweb/data/vn30.csv")

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


#Display
status = st.sidebar.selectbox("Tổng quan thị trường",
                      ['Nhóm dẫn dắt thị trường','Độ rộng thị trường','Biểu đồ vốn hoá'])
if (status == 'Biểu đồ vốn hoá' ):
    st.plotly_chart(vonhoa)
elif (status == 'Độ rộng thị trường'):
    st.plotly_chart(fig)


