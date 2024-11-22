import streamlit as st
import akshare as ak
import time
from openai import OpenAI


def chat_ans(q: str):
    global apikey
    print(apikey)
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.moonshot.cn/v1",
    )

    ## 身份
    msg = [{"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话，同时精通金融、财务、股票等相关经济金融知识。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}]
    
    ## 上传的文件
    if upfile is not None:
        file_obj = client.files.create(file=upfile, purpose="file-extract")
        file_content = client.files.content(file_id=file_obj.id).text
        msg.append({"role": "system", "content": file_content})
        
        
    ## 提问文本    
    msg.append({"role": "user", "content":f"{q}"})
    
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=msg,
        temperature=0.3,
    )
    res = completion.choices[0].message.content
    return res

def stream_data(w: str):
    for ele in w:
        yield ele
        time.sleep(0.02)
       
def getsummary():
    global cont, cont_below_key
    if upfile is None:
        cont_below_key.warning("请先上传文件", icon="⚠️")
        return
    st.session_state.messages.append({"role": "user", "content": "一键总结"})
    cont.chat_message("user").write("一键总结")
    q = sample_prompt+sample
    res = chat_ans(q)
    st.session_state.messages.append(
                {"role": "assistant", "content": res})
    cont.chat_message("assistant").write_stream(stream_data(res))
    return
    
def chat():
    """
    侧边栏chatbot
    """
    global limitlength, upfile, apikey, cont, cont_below_key
    with st.sidebar:
        st.subheader("💬 Chatbot")
        
        apikey = st.text_input("请输入kimi APIKEY", value="", type="password")
        print(apikey)
        cont_below_key = st.container()
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}]
        if len(st.session_state['messages']) > limitlength:
            st.session_state.messages = st.session_state.messages[-limitlength:]
            print("clear msg")
            
        cont = st.container(height=500)
        for msg in st.session_state.messages:
            cont.chat_message(msg["role"]).write(msg["content"])

        cols = st.columns(2)
        cols[0].button("清空历史消息", on_click=lambda: st.session_state.messages.clear(), use_container_width=True)
        cols[1].button("一键总结", on_click=getsummary, use_container_width=True)
        if prompt := st.chat_input():
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            cont.chat_message("user").write(prompt)
            msg = chat_ans(prompt)
            st.session_state.messages.append(
                {"role": "assistant", "content": msg})
            cont.chat_message("assistant").write_stream(stream_data(msg))
        upfile = st.file_uploader("上传文件")

cont_below_key = None
cont = None
limitlength = 50
upfile = None
apikey = None
sample_prompt = "请根据上传的文件，依据下述模板，生成一份关于该公司的投资建议。对于文件中未提供的数据或信息但模板中又需要的，可以自行在回答中省略该部分。模板如下："
sample ='''
当对前公司（替换为具体公司名）综述性的建议如下：
### 资金方面
- 投资活动：支出现金是否较多？公司是处于扩张还是紧缩阶段？
- 筹资活动：
    + 主要资金来源为什么机构？由什么资金支持？筹资获得的资金是否充足且稳定？
    + 财务杠杆比率为？
- 对比行业平均情况，该企业资金状况如何？
- 由资产资本表，（当前资产结构体现公司为重/轻资产公司）。资产策略属于（匹配型/稳健型/激进型）。
- 可能存在的风险“雷区”有哪些？
### 股权价值
- 经营利润为？营业费用为？实际利润情况如何？实际利润比先前有所增加/下降，实际利润与行业平均情况对比如何？
- 由此带来的股权价值增加额/比例为？
### 综合分析
- 提供一些对该企业的综合分析？
- 经营资产的管理销量如何？
- 经营周期处于什么阶段？
- 股东收益及股东相关信息方面怎么评价？
- 现金流量方面状况如何？
- 流动性问题可能存在的部分有？
基于以上信息，该公司适合什么类型的投资者？主要风险在于？总体的投资建议是？
'''