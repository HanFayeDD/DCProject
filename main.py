import streamlit as st
from page1.mainpage1 import mainpage1


st.set_page_config(page_title="Demov1", layout="wide")
pg = st.navigation([
    st.Page(mainpage1, title="page1", icon="🤓")
])

pg.run()