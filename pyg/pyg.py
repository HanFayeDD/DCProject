import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import pygwalker as pyg

def pygchat():
    st.title("use pygwalker😍")

    uploaded_file = st.file_uploader("Your csv data")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer()
    
    cols = st.columns(1)
    with cols[0]:
        st.subheader("chatbot")
        st.subheader("data")
        data = {
            '年份': [2020, 2021, 2022],
            '销量': [100, 200, 300]
        }
        df = pd.DataFrame(data)
        pyg1 = StreamlitRenderer(df)
        pyg1.explorer()