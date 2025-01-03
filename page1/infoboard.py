import streamlit as st
import akshare as ak
from datetime import datetime, timedelta
import pandas as pd
import random


class Data():
    """
    3*3信息看板
    Params:
        code (list[str]): 股票代码
        sepdays (int): 时间间隔往前寻找的长度
        begindays (str): 开始时间
        endays (str): 结束时间默认是当前日期
    """
    codepool: list[str] = []
    code: list[str] = ['000001', '000002', '000028',
                       '000004', '000050', '000050',
                       '000001', '000002', '000028']
    dflist = []
    sepdays: int = 90
    endays: str = datetime.now().strftime('%Y%m%d')
    begindays: str = (datetime.now() - timedelta(days=sepdays)
                      ).strftime('%Y%m%d')
    colheight = 380  # 方格的高
    chartheight = 250  # 图表的高

    def __init__(self) -> None:
        pass  # 只有在Date()创建一个实例的时候会执行

    @staticmethod
    def infoboard():
        '''
        信息看板部分
        '''
        st.title("数据看板")
        # TODO: 添加换一批按钮，目前仅随机打乱
        if st.button("换一批"):
            Data.code = random.sample(Data.codepool, 9)
            print(f"new code list {Data.code}")
            Data.get_data()
            # return 如果添加return按下按钮后就只剩下按钮了因为此函数已经结束了
        row1 = st.columns(3)
        row2 = st.columns(3)
        row3 = st.columns(3)
        cnt = 0
        if len(Data.dflist) == 0:
            Data.get_data()
        for col in row1 + row2 + row3:
            tile = col.container(height=Data.colheight)
            tile.subheader(f"{Data.code[cnt]}")
            data = Data.dflist[cnt]
            cnt += 1
            with tile:
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                    ["开盘收盘", "最高最低", "成交量", "成交额", "涨跌幅", "换手率"])
                Data.draw_tab(tab1, data, 0, [2, 3])
                Data.draw_tab(tab2, data, 0, [4, 5])
                Data.draw_tab(tab3, data, 0, [6])
                Data.draw_tab(tab4, data, 0, [7])
                Data.draw_tab(tab5, data, 0, [9])
                Data.draw_tab(tab6, data, 0, [11])

    @classmethod
    # @st.cache_data
    def get_data(cls, tarcode:str=None):
        '''
        根据类属性中的code获取数据
        Yields:
            pd.Dataframe:从akshare中获取的数据
        '''
        Data.dflist = []
        print("run get_data")
        if tarcode is None:
            for code in cls.code:
                data = ak.stock_zh_a_hist(symbol=code, period="daily",
                                        start_date=cls.begindays,
                                        end_date=cls.endays, adjust="qfq")
                Data.dflist.append(data)
            return 1
        elif tarcode is not None:
            try:
                res = ak.stock_zh_a_hist(symbol=tarcode, period="daily",
                                        start_date=cls.begindays,
                                        end_date=cls.endays, adjust="qfq")
                return res
            except Exception as e:
                return None

    @classmethod
    def draw_tab(cls, tab, df: pd.DataFrame, x: int, y: list[int]):
        """_summary_
        画出每一个tab中的图像
        Args:
            tab (st.tab): tab对象
            df (pd.DataFrame): df值
            x (int): x轴的列数
            y (list[int]): y轴的列数
        """
        with tab:
            st.line_chart(
                df,
                x=df.columns[x],
                y=df.columns[y],
                color=["#FF0000"] if len(y) == 1 else [
                    "#FF0000", "#0000FF"],  # Optional
                height=Data.chartheight,
                width=100
            )