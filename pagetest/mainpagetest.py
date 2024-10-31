import streamlit as st
import pandas as pd

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

a = 1
