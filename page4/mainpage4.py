import streamlit as st
import mdpd
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer



def mainpage4():
    st.title('绘图(markdown or 导入文件)')
    # if st.button("清空数据"):
    #     global df, rich_text
    #     df = None
    #     rich_text = rich_text_eg
    tab_md, tabdf = st.tabs(['markdown表格', '导入表格'])
    with tab_md:
        input_md()
    with tabdf:
        input_file()
    try:
        if df is not None:
            use_pygwalker()
    except ZeroDivisionError as e:
        st.error("请输入正确的数据")
    
    
def use_pygwalker():
    st.subheader("pygwalker")
    pyg = StreamlitRenderer(df, theme_key='streamlit', appearance='light')
    pyg.explorer()
    
def get_md_text():
    """
    在rich_text_eg和sidechat ocr_res中选择
    """    
    if st.session_state.ocr_res is not None:
        print("use ocr_res")
        return st.session_state.ocr_res
    else:
        print("use rich_text_eg")
        return rich_text_eg
    
def input_md():
    global rich_text, df, df_dtype
    st.subheader("markdown表格")
    # st.markdown(md_tips)
    rich_text = st.text_area('输入markdown表格', value=get_md_text(), height=200)
    tab_md, tab_df, tab_dtype = st.tabs(['markdown table', 'Dataframe', '数据类型'])
    with tab_md:
        st.markdown(rich_text)
    with tab_df:
        df = mdpd.from_md(rich_text)
        df_type, new_cols = get_df_type(df.columns.to_list())
        df.columns = new_cols
        df = df.astype(df_type)
        st.dataframe(df)
        print("df change in md")
    with tab_dtype:
        st.write(df_type)

def input_file():
    global df
    st.subheader("导入文件")
    file = st.file_uploader("上传文件", type=["csv", "xlsx"])
    if file is not None:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                raise ValueError('文件类型错误')
            print("df change in file_uploader")
        except:
            st.error('文件读取错误')
        file_tabs = st.tabs(['Dataframe', '数据类型'])
        with file_tabs[0]:
            st.dataframe(df)
        with file_tabs[1]:
            st.write(df.dtypes)
    

    
def get_df_type(col_list):
    df_type = dict()
    new_cols = []
    for ele in col_list:
        new_cols.append(ele.strip())
        for type in ['int', 'float32', 'str']: 
            try:
                _ = df[ele].astype(type)
                df_type[ele.strip()] = type
                break
            except:
                pass
    return df_type, new_cols


# md_tips='''
# 在md表头中注意添加数据类型
# - 字符类型末尾添加 :green-background[_str]
# - 数值float类型末尾添加 :green-background[_flt]
# - 数值int类型末尾添加 :green-background[_int]'''

rich_text_eg = '''| year    | output |
| --------- | ----------- |
| 2001年 | 1        |
| 2002年 | 2        |
| 2003年 | 2        |
| 2004年 | 2        |
| 2005年 | 2        |
'''



rich_text = ''
df = None
