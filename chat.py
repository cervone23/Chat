import streamlit as st
from streamlit_chat import message
import openai
from PIL import Image
import base64

st.set_page_config(
    page_title = "Blackstone ChatGPT Chatbot",
    page_icon = Image.open("favicon.png")
)

def image_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
image_local('image.png')    

###############################################################################
    
openai.api_key = st.secrets['api_key']

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
    
if 'prompt_text' not in st.session_state:
    st.session_state['prompt_text'] = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n"

def answer_ChatGPT(question):
    st.session_state['prompt_text'] += f"Human: {question}\nAI:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    response_text = response.choices[0].text
    st.session_state['prompt_text'] += f" {response_text}\n"
    return response_text

def input_and_clear():
    st.session_state['user_input'] = st.session_state['input']
    st.session_state['input'] = ""

# layout
st.header("Blackstone & ChatGPT - Chatbot Demo")
st.text_input("**input message :**", key="input", on_change=input_and_clear)

if st.session_state['user_input']:
    output = answer_ChatGPT(st.session_state['user_input'])
    st.session_state.past.append(st.session_state['user_input'])
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], seed=86, key=str(i))
        message(st.session_state['past'][i], is_user=True, 
                avatar_style='fun-emoji', key=str(i) + '_user')
