import openai
import streamlit as st

st.title("Chat Bot (GPT-4)")

connection = {
    "api_key": "",
    "api_version": "2023-05-15",
    "azure_endpoint": "",
}

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_api_base = st.sidebar.text_input('OpenAI API Base', value='https://chatgpt-canadaeast.openai.azure.com/')
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=4096, value=500, step=1)
top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        connection["api_key"] = openai_api_key
        connection["azure_endpoint"] = openai_api_base
        client = openai.AzureOpenAI(**connection)
        for response in client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model=st.session_state["openai_model"],
            temperature=temperature,
            top_p=top_p,
            n=1,
            stream=True,
            stop=None,
            max_tokens=max_tokens,
            ):
            delta = response.choices[0].delta.content if isinstance(response.choices[0].delta.content, str) else ""
            full_response += delta
            message_placeholder.markdown(full_response)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})