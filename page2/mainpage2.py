import streamlit as st
from page2.company_info import info

def mainpage2():
    st.title("Introduce")
    info.get_info()
    