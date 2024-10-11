import streamlit as st
from page1.mainpage1 import mainpage1
from page2.mainpage2 import mainpage2

st.set_page_config(page_title="Demov1", layout="wide")
pg = st.navigation([
    st.Page(mainpage1, title="page1", icon="🤓"),
    st.Page(mainpage2, title="page2", icon="🥰")
])

pg.run()