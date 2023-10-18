import streamlit as st
from settings import*
from streamlit_option_menu import option_menu
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub
from langchain.chains import ConversationChain

# streamlit run AI_chatBots_clones.py


def generate_response_HugHub(prompt, _llm):
   
    memory = ConversationBufferMemory(return_messages=True)

    conversation_buf = ConversationChain(
        llm=_llm,
        memory=memory)
    answer = conversation_buf.predict(input=prompt)
    
    return answer

st.set_page_config(page_title=TITLE,
    page_icon="AI ChatBot",
    layout="wide")

HUGGINGFACEHUB_API_TOKEN ="Your_huggingfacehub_api_token"

with st.sidebar:
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    temp_val = st.slider("💡 AI Creativity", min_value=0.0, max_value=1.0, value=0.2, format="")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "How can i assist you today ?"}]

col1, col2, col3 = st.columns([25,50,25])
with col2:
    selected_model = option_menu(menu_title=None, options=['Mstral-7B', 'Zephyr-7B', 'Falcon-7B'], 
        default_index=0, orientation="horizontal",
        icons=["empty", "empty", "empty"],
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px", "--hover-color": "#805E83"}
        })
    
if selected_model == 'Mstral-7B':
    llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1", model_kwargs={"temperature":temp_val, "max_length":512})
elif selected_model == 'Zephyr-7B':
    llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-alpha", model_kwargs={"temperature":temp_val, "max_length":512})
else:
    llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct", model_kwargs={"temperature":temp_val, "max_length":512})

if "llm" not in st.session_state:
    st.session_state.llm = selected_model


if st.session_state.llm != selected_model :
    st.session_state.messages = [{"role": "assistant", "content": "How can i assist you today ?"}]




if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can i assist you today ?"}]


# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input(placeholder="Ask your questions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("user"):
        st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":

        with st.chat_message("assistant"):
            with st.spinner('Tinking...'):

                response = generate_response_HugHub(prompt, llm)

                st.write(response)

        message = {"role": "assistant", "content": response}

        st.session_state.messages.append(message)