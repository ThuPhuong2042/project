import streamlit as st
import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/ThuPhuong2042/project/main/datangtruong.csv')
st.table(data)
