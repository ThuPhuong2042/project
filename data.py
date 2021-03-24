import streamlit as st
import pandas as pd
import numpy as np

data = pd.read_csv('https://raw.githubusercontent.com/ThuPhuong2042/project/main/datangtruong.csv')
st.write(data)
