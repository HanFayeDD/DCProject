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


class CustSearch():

    tarcode: str = None
    tardf: pd.DataFrame = None

    # 主营df
    years: list = None
    maindf: pd.DataFrame = None

    def __init__(self) -> None:
        pass

    @classmethod
    def panel(cls):
        st.title('自定义查询')
        CustSearch.tarcode = st.text_input("输入查询代码", "000001")
        
        st.subheader("基本信息(page2重复)")
        with st.expander("基本信息", expanded=False, icon="🚆"):  
            CustSearch.show_base_info()
        
        st.subheader("股票信息查询")
        temp = Data.get_data(CustSearch.tarcode)
        if temp is not None:
            CustSearch.tardf = temp
            with st.expander("获取到的数据", expanded=False, icon="🚂"):
                st.dataframe(CustSearch.tardf, use_container_width=True)
            CustSearch.draw()
        else:
            st.error('查询失败', icon="🚨")
            
        st.subheader("主营构成")
        res = cls.getmaindf()
        if res == -1:
            st.error('查询失败', icon="🚨")
        else:
            with st.expander("获取到的数据", expanded=False, icon="🚂"):
                st.dataframe(CustSearch.maindf, use_container_width=True)
            cls.years = cls.maindf['报告期'].unique().tolist()
            cls.years = [ele for ele in cls.years if ele.endswith('年度')]
            cls.years.sort()
            category = cls.maindf['分类方向'].unique().tolist()
            print(category)
            hang_num = math.ceil(len(category)/2)
            # pietabs = st.tabs(category)
            for i in range(hang_num):
                if 2*i + 1 == len(category):
                    cls.drawtimeline(category[-1])
                    break
                pie_tabs = st.columns(2)
                for j in range(2):
                    if(i*2+j >= len(category)):
                        break
                    with pie_tabs[j]:
                        cls.drawtimeline(category[i*2+j])
        
    @classmethod
    def getmaindf(cls):
        try:
            cls.maindf = ak.stock_zygc_ym(symbol=cls.tarcode)
            return 0
        except AttributeError:
            return -1

    @classmethod
    def drawtimeline(cls, groupby_name: str):
        tl = Timeline()
        tl.add_schema()
        print(groupby_name)
        for year in cls.years:
            df = cls.maindf[cls.maindf['报告期'] == year]
            df = df[df['分类方向'] == groupby_name]
            df = df.loc[df['分类'] != '合计']
            cate = df['分类'].to_list()
            data = df['营业收入'].to_list()
            print(cate)
            print(data)
            if len(data)==0 or len(cate)==0:
                continue
            data, danwei = CustSearch.get_danwei(data)
            print(data, danwei)
            pie = (Pie(init_opts=opts.InitOpts(theme='shine'))
                .add(f'单位({danwei})', [list(z) for z in zip(cate, data)],  radius=["35%", "75%"])
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{groupby_name}",pos_left='center',pos_bottom='center', 
                                                           title_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                                 legend_opts=opts.LegendOpts(is_show=False))
                )
            tl.add(pie, year)
        st_pyecharts(tl, height='450px')

    @staticmethod
    def get_danwei(data: list[str]):
        # print(data)
        if len(data) == 0:
            raise ValueError("data数组长度为0")
        first = data[0]
        idx = len(first)-1
        while not (first[idx].isdigit() or first[idx] == '.'):
            idx -= 1
        danwei = first[idx+1:]
        # print("单位:", danwei)
        for ele in data:
            if not ele.endswith(danwei):
                raise ValueError("单位不一致")
        res_data = [ele[:-len(danwei)] for ele in data]
        return res_data, danwei

    @classmethod
    def draw(cls):
        cols = st.columns(4)
        df23 = CustSearch.tardf.iloc[:, [0, 2, 3]]
        data = df23.melt(id_vars=['日期'], var_name='开盘/收盘', value_name='价格')
        c0 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='价格',
            color='开盘/收盘'
        )
        cols[0].altair_chart(c0, use_container_width=False)

        df45 = CustSearch.tardf.iloc[:, [0, 4, 5]]
        data = df45.melt(id_vars=['日期'], var_name='最高/最低', value_name='价格')
        c1 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='价格',
            color='最高/最低'
        )
        cols[1].altair_chart(c1, use_container_width=False)

        df6 = CustSearch.tardf.iloc[:, [0, 6]]
        c2 = alt.Chart(df6).mark_line().encode(
            x='日期',
            y='成交量'
        )
        cols[2].altair_chart(c2, use_container_width=False)

        df8_11 = CustSearch.tardf.iloc[:, [0, 8, 9, 10, 11]]
        data = df8_11.melt(id_vars=['日期'], var_name='率', value_name='百分率')
        c1 = alt.Chart(data).mark_line().encode(
            x='日期',
            y='百分率',
            color='率'
        )
        cols[3].altair_chart(c1, use_container_width=False)

    @classmethod
    def show_base_info(cls):
        info_df = ak.stock_profile_cninfo(symbol=cls.tarcode)
        if info_df.shape[0] == 0:
            st.error(f'{cls.tarcode}代码不存在', icon="🚨")
            return
        len = info_df.shape[1]
        for i in range(len):
            if info_df.iloc[0, i] is None:
                continue
            st.write(info_df.columns[i], info_df.iloc[0, i])