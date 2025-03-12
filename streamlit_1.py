# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 18:13:10 2025

@author: Richa
"""

import streamlit as st
from openai import OpenAI

st.title("ChatGPT-like Clone")

client = OpenAI(api_key="your_open_AI_Key")


#Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  #empty list to keep session state

#Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
#React to user Input
prompt = st.chat_input("what's up?")
if prompt:
    #display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    #Add user message to chat history
    st.session_state.messages.append({"role":"user", "content":prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response =""
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}  # To save conversation
                for m in st.session_state.messages
            ],
            stream=True,  # To simulate typing effect
        )
        # Stream the response
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)  # Display full response
    st.session_state.messages.append({"role": "assistant", "content": full_response})  # Conversation saved with session_state for future interaction