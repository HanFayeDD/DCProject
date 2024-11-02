import streamlit as st
import mdpd


def mainpage4():
    st.title('绘图(markdown or 导入文件)')
    tab_md, tabdf = st.tabs(['markdown表格', '导入表格'])
    with tab_md:
        input_md()
    with tabdf:
        input_df()


def input_md():
    global rich_text, df, df_dtype
    st.subheader("markdown表格")
    st.markdown(md_tips)
    rich_text = st.text_area('输入markdown表格', value=rich_text_eg, height=200)
    st.subheader("markdown表格预览")
    st.markdown(rich_text)
    st.subheader("markdown表格 > Dataframe")
    df = mdpd.from_md(rich_text)
    df_type, new_cols = get_df_type(df.columns.to_list())
    df = df.astype(df_type)
    df.columns = new_cols
    st.dataframe(df)
    print(df.dtypes)
    
def get_df_type(col_list):
    print(col_list)
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
    print(new_cols)
    return df_type, new_cols

def input_df():
    return

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
