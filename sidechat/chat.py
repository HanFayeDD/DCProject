import streamlit as st
import akshare as ak
import time

def chat_ans(q:str):
    res = ak.nlp_answer(question=q)
    if upfile is not None:
        res = f"🤖🤖echo file {upfile.name}" + res
    return res

def stream_data(w:str):
    for ele in w:
        yield ele
        time.sleep(0.02)

def chat():
    """
    侧边栏chatbot
    """
    global limitlength, upfile
    with st.sidebar:
        st.subheader("💬 Chatbot")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        if len(st.session_state['messages']) > limitlength:
            st.session_state.messages = st.session_state.messages[-limitlength:]
            print("clear msg")
        cont = st.container(height=500)
        for msg in st.session_state.messages:
            cont.chat_message(msg["role"]).write(msg["content"])

        st.button("清空历史消息", on_click=lambda: st.session_state.messages.clear(), use_container_width=True)
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            cont.chat_message("user").write(prompt)
            msg = chat_ans(prompt)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            cont.chat_message("assistant").write_stream(stream_data(msg))
        upfile = st.file_uploader("上传文件")

limitlength = 50
upfile = None