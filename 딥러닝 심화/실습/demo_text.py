# demo.py
import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_model():
    return pipeline(task="text-generation", model="gpt2")


model = load_model()

text = st.text_input("텍스트 입력", value="Machine learning is")
if text:
    result = model(
        text_inputs=text,
        max_length=30,
        num_return_sequences=3,
        pad_token_id=model.tokenizer.eos_token_id,
    )
    st.write(result)