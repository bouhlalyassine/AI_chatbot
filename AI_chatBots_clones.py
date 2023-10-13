import streamlit as st
from settings import*
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import openai
# streamlit run AI_chatBots_clones.py

st.set_page_config(page_title=TITLE,
    layout="wide")

with st.sidebar :
    nav_menu = option_menu(menu_title=None, options=['Home', 'Llama', 'OpenAI'], 
        
        default_index=0, orientation="vertical",
        icons=["house", "robot", "robot"],
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"2px", "--hover-color": "#805E83"}
        })

if nav_menu == 'Home':
    st.markdown("<h2 style=\
        'text-align : center'>\
        AI ChatBot</h2>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    colpi1, colpi2 = st.columns([75, 25], gap="small")
    with colpi1:
        st.info("\
            This app is a simple clone of two LLMs (Llama-2 & OpenAI-3.5) AI Chatbots using specific API keys :\
            \n● Llama-2 : Since this LLM is open source, we must use a hosting service, in our case, we used Replicate.\
            \n● OpenAI : We can simply use an OpenAI API key.\
            \n\nTo build a chatbot using srtreamlit, please check the following blog posts : \
            [Llama-2](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)\
             & \
            [OpenAI](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)\
            \n\n►To test the clones, please check the left side menu")
    
    with colpi2:
        st.markdown("<br>", unsafe_allow_html=True)
        lottie_dashb = load_lottiefile(lottie_robot)
        st_lottie(
            lottie_dashb,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=170)


if nav_menu == 'Llama':
    col1, col2, col3 = st.columns([25,50,25])
    with col2:
        selected_model = option_menu(menu_title=None, options=['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], 
            default_index=0, orientation="horizontal",
            icons=["empty", "empty", "empty"],
            styles={
                "container": {"padding": "0!important"},
                "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px", "--hover-color": "#805E83"}
            })
        
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

    replicate_api = st.sidebar.text_input('Enter Replicate API key :', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
        st.sidebar.warning('Enter your API Key', icon='⚠️')
    else:
        st.sidebar.success('API key provided', icon='✅')

    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    
    # User-provided prompt
    # The := is to check if prompt is not "none" we can also do it like :
    # prompt = st.chat_input('message')*
    # if prompt: ...
    if prompt := st.chat_input(disabled=not replicate_api, placeholder="Write you message here"): # disable the chat input if the api is not in provided
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
    try :
        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llama2_response(prompt, llm)
                    placeholder = st.empty()
                    full_response = ''
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)
    except:
        st.error("API calls quota exceeded")

    #st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


if nav_menu == "OpenAI":
    with st.sidebar:
        openai.api_key = st.text_input('Enter OpenAI API key:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Enter your API Key', icon='⚠️')
        else:
            st.success('API key provided', icon='✅')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    try :
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages], stream=True):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        st.error("API calls quota exceeded")

    #st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)