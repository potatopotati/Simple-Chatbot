import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
API_KEY = os.getenv('API_KEY')

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

def get_response(chat_history):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Answer clearly and accurately in plain text. Do not include source citations like [1], [2], etc., unless the user asks for them."
            )
        }
    ]
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({"role": "assistant", "content": msg.content})

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages
    )
    return response.choices[0].message.content

#print chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    else:
        with st.chat_message("ai"):
            st.markdown(message.content)

#user new query
user_query = st.chat_input("Ask anything")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("human"):
        st.markdown(user_query)
    with st.chat_message("ai"):
        ai_response = get_response(st.session_state.chat_history) 
        st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))
