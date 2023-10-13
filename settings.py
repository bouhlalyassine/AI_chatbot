import json
from pathlib import Path
import requests
import streamlit as st
import replicate

TITLE = "AI ChatBot"
PAGE_ICON ="ico_potfolio.ico"


current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()


lottie_robot = current_dir / "files" /  "robot.json"

def load_lottiefile(filepath : str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Function for generating LLaMA2 response
# Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input, llm):
    pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            pre_prompt += "User: " + dict_message["content"] + "\n\n"
        else:
            pre_prompt += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
        input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ",
        "temperature":0.2, "top_p":0.8, "max_length":1024, "repetition_penalty":1})
    return output


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]