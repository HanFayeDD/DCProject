import streamlit as st 
import akshare as ak 
import pandas as pd

class info():
    code:str = ''
    df:pd.DataFrame = pd.DataFrame()
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_info(cls):
        try:
            with st.container():
                info.code = st.text_input("输入代码", "000001")
                if len(info.code) != 6:
                    st.error('代码格式错误', icon="🚨")
                else:
                    info.print_stock_profile_cninfo()
        except Exception as e:
            print(e)
            st.error('出现错误', icon="🚨")
            
    
    @staticmethod
    def print_stock_profile_cninfo():
        info.df = ak.stock_profile_cninfo(symbol=info.code)
        if info.df.shape[0] == 0:
            st.error(f'{info.code}代码不存在', icon="🚨")
            return
        len = info.df.shape[1]
        for i in range(len):
            if info.df.iloc[0,i] is None:
                continue
            st.write(info.df.columns[i], info.df.iloc[0,i])
        
        