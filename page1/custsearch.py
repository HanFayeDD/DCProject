import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from page1.infoboard import Data

class CustSearch():
    
    tarcode:str = None
    tardf:pd.DataFrame = None
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def panel(cls):
        st.title('自定义查询')
        CustSearch.tarcode = st.text_input("输入查询代码", "000001")
        temp =  Data.get_data(CustSearch.tarcode) 
        if temp is not None:
            CustSearch.tardf = temp
            with st.expander("获取到的数据", expanded=True, icon="🚂"):
                st.dataframe(CustSearch.tardf, use_container_width=True)
            CustSearch.draw()
        else:
            st.error('查询失败', icon="🚨")
            
                
    @classmethod
    def draw(cls):
        cols = st.columns(4)
        df23 = CustSearch.tardf.iloc[:,[0, 2, 3]]
        data = df23.melt(id_vars=['日期'], var_name='开盘/收盘', value_name='价格')
        c0 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='价格',
            color='开盘/收盘'
        )
        cols[0].altair_chart(c0, use_container_width=False)
        
        df45 = CustSearch.tardf.iloc[:,[0, 4, 5]]
        data = df45.melt(id_vars=['日期'], var_name='最高/最低', value_name='价格')
        c1 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='价格',
            color='最高/最低'
        )
        cols[1].altair_chart(c1, use_container_width=False)
        
        df6 = CustSearch.tardf.iloc[:,[0, 6]]
        c2 = alt.Chart(df6).mark_line().encode(
            x='日期',
            y='成交量'
        )
        cols[2].altair_chart(c2, use_container_width=False)
        
        df8_11 = CustSearch.tardf.iloc[:,[0, 8, 9, 10, 11]]
        data = df8_11.melt(id_vars=['日期'], var_name='率', value_name='百分率')
        c1 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='百分率',
            color='率'
        )
        cols[3].altair_chart(c1, use_container_width=False)
        
        