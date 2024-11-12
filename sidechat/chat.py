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


    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话，同时精通金融、财务、股票等相关经济金融知识。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": f"{q}"}
        ],
        temperature=0.3,
    )
    res = completion.choices[0].message.content
    if upfile is not None:
        res = f"🤖🤖echo file {upfile.name}" + res
    return res

def stream_data(w: str):
    for ele in w:
        yield ele
        time.sleep(0.02)

def chat():
    """
    侧边栏chatbot
    """
    global limitlength, upfile, apikey
    with st.sidebar:
        st.subheader("💬 Chatbot")
        
        apikey = st.text_input("请输入kimi APIKEY", value="", type="password")
        print(apikey)
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}]
        if len(st.session_state['messages']) > limitlength:
            st.session_state.messages = st.session_state.messages[-limitlength:]
            print("clear msg")
        cont = st.container(height=500)
        for msg in st.session_state.messages:
            cont.chat_message(msg["role"]).write(msg["content"])

        st.button("清空历史消息", on_click=lambda: st.session_state.messages.clear(
        ), use_container_width=True)
        if prompt := st.chat_input():
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            cont.chat_message("user").write(prompt)
            msg = chat_ans(prompt)
            st.session_state.messages.append(
                {"role": "assistant", "content": msg})
            cont.chat_message("assistant").write_stream(stream_data(msg))
        upfile = st.file_uploader("上传文件")


limitlength = 50
upfile = None
apikey = None