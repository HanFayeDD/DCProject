import streamlit as st 
import akshare as ak
from datetime import datetime, timedelta

class Data():
    """
    3*3信息看板
    Params:
        code (list[str]): 股票代码
        sepdays (int): 时间间隔往前寻找的长度
        begindays (str): 开始时间
        endays (str): 结束时间默认是当前日期
    """
    code:list[str] = ['000001', '000002','000028',
                      '000004', '000050','000050',
                      '000001', '000002','000028'] 
    sepdays:int = 60
    begindays:str = ''
    endays:str = ''
    
    def __init__(self) -> None:        
        Data.begindays = (datetime.now() - timedelta(days=Data.sepdays)).strftime('%Y%m%d')
        Data.endays = datetime.now().strftime('%Y%m%d')
        print(Data.begindays, Data.endays)

    @staticmethod
    def infoboard():
        '''
        信息看板部分
        '''
        st.title('Part1')
        row1 = st.columns(3)
        row2 = st.columns(3)
        row3 = st.columns(3)

        cnt = 0
        datagen = Data().get_data()
        for col in row1 + row2 + row3:
            tile = col.container(height=350)
            tile.subheader(f"{Data.code[cnt]}")
            cnt += 1
            data = next(datagen).iloc[:,:3]
            with tile:
                st.line_chart(
                    data,
                    x=data.columns[0],
                    y=data.columns[1:3],
                    color=["#FF0000", "#0000FF"],  # Optional
                    height=300,
                    width=100
                )
        
    @classmethod
    def get_data(cls):
        '''
        根据类属性中的code获取数据
        Yields:
            pd.Dataframe:从akshare中获取的数据
        '''
        for code in cls.code:
            try:
                data = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                        start_date=cls.begindays, 
                                        end_date=cls.endays, adjust="qfq")
                yield data
            except Exception as e:
                print(f'获取{code}出错')



    