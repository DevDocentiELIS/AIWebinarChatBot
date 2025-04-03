import streamlit as st
import requests

API_URL = "http://localhost:5000/ask"

st.title("Webinar ELIS Bot")
st.markdown("Chiedimi qualcosa riguardo al Master Intelligenza Artificiale e Machine Learning di ELIS")

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

    try:
        response = requests.post(API_URL, json={"question": user_input})

        if response.status_code == 200:
            answer = response.json().get("answer", "No response received.")
        else:
            answer = f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        answer = f"API request failed: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
