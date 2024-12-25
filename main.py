import streamlit as st
from page1.mainpage1 import mainpage1
from page2.mainpage2 import mainpage2 
from page3.mainpage3 import mainpage3
from page4.mainpage4 import mainpage4
from pyg.pyg import pygchat
from pagetest.mainpagetest import mainpagetest 
from sidechat.chat import chat

def welcome():
    st.title("Welcome")

st.set_page_config(page_title="Demov1", layout="wide")
pg = st.navigation([
    st.Page(welcome, title="Welcome", icon="🤗"),
    st.Page(mainpagetest, title="测试页", icon="🤗"),
    st.Page(mainpage1, title="page1", icon="🤓"),
    st.Page(mainpage2, title="page2", icon="🥰"),
    st.Page(mainpage3, title="page3", icon="🥰"),
    st.Page(mainpage4, title="page4", icon="🤔"),
    st.Page(pygchat, title="use pygwalker", icon="✔️"),
])

chat()

pg.run()