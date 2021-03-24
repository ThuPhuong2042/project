import streamlit as st
import pandas as pd

data = pd.read_csv('C:/Users/ThuPhuong/PycharmProjects/dictionaryweb/datangtruong.csv')
st.write(data)