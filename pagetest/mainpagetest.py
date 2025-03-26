import streamlit as st
import pandas as pd
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import akshare as ak
from page1.infoboard import Data
from pyecharts.charts import *
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import math
import random
import datetime
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"

def mainpagetest():
    if 'maintest_exe' not in st.session_state:
        st.session_state.maintest_exe = False
    if not st.session_state.maintest_exe: ##只执行一次
        st.title("测试页")
        st.write("这是一个测试页")
        print("maintest_exe")
        st.session_state.maintest_exe = True
    part1()
    part2()
    part3()
    global a
    if st.button("add"):
        a += 1
    st.write(a)
    
    x = list(range(100))
    y = list(range(100))
    df = pd.DataFrame(dict(x=x, y=y))
    st.line_chart(data=df, x='x', y='y')
    print("line")

    
def part1():
    if st.button("part1"):
        st.write("part1")
        print("part1")
    print("part1")

def part2():
    if st.button("part2"):
        st.write("part2")
        print("part2")

def part3():
    words = [
    ("hey", 230),
    ("jude", 124),
    ("dont", 436),
    ("make", 255),
    ("it", 247),
    ("bad", 244),
    ("Take", 138),
    ("a sad song", 184),
    ("and", 12),
    ("make", 165),
    ("it", 247),
    ("better", 182),
    ("remember", 255),
    ("to", 150),
    ("let", 162),
    ("her", 266),
    ("into", 60),
    ("your", 82),
    ("heart", 173),
    ("then", 365),
    ("you", 360),
    ("can", 282),
    ("start", 273),
    ("make", 265),
    ("吃", 100)
]
    wc = (
        WordCloud()
        .add("", words)
    )
    st_pyecharts(wc)

a = 1
