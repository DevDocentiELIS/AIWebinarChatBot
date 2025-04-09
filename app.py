import streamlit as st
import requests

API_URL = "http://localhost:5000/ask"

st.title("Webinar ELIS Bot")
st.markdown("Chiedimi qualcosa riguardo al Master Intelligenza Artificiale e Machine Learning di ELIS")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Chiedimi qualcosa che riguarda il Master AI e ML di ELIS...")

if user_input:
    # Add the user message to the session
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create a placeholder and also prepare the new assistant message
    placeholder = st.empty()
    full_answer = ""

    try:
        with requests.post(API_URL, json={"question": user_input}, stream=True) as response:
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=128, decode_unicode=True):
                    if chunk:
                        full_answer += chunk
                        # Update the placeholder with the streaming content
                        placeholder.markdown(full_answer)
            else:
                full_answer = f"Error: {response.status_code} - {response.text}"
                placeholder.markdown(full_answer)
    except requests.exceptions.RequestException as e:
        full_answer = f"API request failed: {e}"
        placeholder.markdown(full_answer)

    # Instead of appending a new chat message, update the last entry
    st.session_state.messages.append({"role": "assistant", "content": full_answer})
    # Remove the separate message block, as the placeholder already served to display the streaming answer.
