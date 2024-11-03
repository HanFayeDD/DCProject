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
    if df is not None:
        use_pygwalker()
    
def use_pygwalker():
    st.subheader("pygwalker")
    pyg = StreamlitRenderer(df, theme_key='streamlit')
    pyg.explorer()
    
# @st.cache_resource
def input_md():
    global rich_text, df, df_dtype
    st.subheader("markdown表格")
    st.markdown(md_tips)
    rich_text = st.text_area('输入markdown表格', value=rich_text_eg, height=200)
    tab_md, tab_df, tab_dtype = st.tabs(['markdown table', 'Dataframe', '数据类型'])
    with tab_md:
        st.markdown(rich_text)
    with tab_df:
        df = mdpd.from_md(rich_text)
        df_type, new_cols = get_df_type(df.columns.to_list())
        df = df.astype(df_type)
        df.columns = new_cols
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
    st.dataframe(df)
    

    
def get_df_type(col_list):
    new_cols = []
    df_type = dict()
    for ele in col_list:
        if ele.endswith('_str'):
            new_cols.append(ele[:-4])
            df_type[ele] = 'str'
        elif ele.endswith('_int'):
            new_cols.append(ele[:-4])
            df_type[ele] = 'int'
        elif ele.endswith('_flt'):
            new_cols.append(ele[:-4])
            df_type[ele] = 'float32'
        else:
            raise ValueError('类型错误')
    return df_type, new_cols


md_tips='''
在md表头中注意添加数据类型
- 字符类型末尾添加 :green-background[_str]
- 数值float类型末尾添加 :green-background[_flt]
- 数值int类型末尾添加 :green-background[_int]'''

rich_text_eg = '''| year_str    | output_int |
| --------- | ----------- |
| 2001 | 1        |
| 2002 | 2        |
| 2003 | 2        |
| 2004 | 2        |
| 2005 | 2        |
'''
rich_text = ''
df = None
