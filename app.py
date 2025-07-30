import streamlit as st
import requests

API_URL = "http://localhost:5000/ask"

st.title("Webinar ELIS Bot")
st.markdown("Chiedimi qualcosa riguardo alle fonti a mia disposizione")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Chiedimi qualcosa che riguarda il Master AI e ML di ELIS...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    placeholder = st.empty()
    full_answer = ""

    try:
        with requests.post(API_URL, json={"question": user_input}, stream=True) as response:
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=128, decode_unicode=True):
                    if chunk:
                        full_answer += chunk
                        placeholder.markdown(full_answer)
            else:
                full_answer = f"Error: {response.status_code} - {response.text}"
                placeholder.markdown(full_answer)
    except requests.exceptions.RequestException as e:
        full_answer = f"API request failed: {e}"
        placeholder.markdown(full_answer)

    st.session_state.messages.append({"role": "assistant", "content": full_answer})
