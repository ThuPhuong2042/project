import streamlit as st
import pandas as pd
import base64

data = pd.read_csv('https://raw.githubusercontent.com/ThuPhuong2042/project/main/datangtruong.csv')
st.write(data)

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'

if st.button('Dơwnload'):
    get_table_download_link(data)
