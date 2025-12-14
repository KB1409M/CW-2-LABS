# chatgpt_bot.py
import streamlit as st
from openai import OpenAI
import httpx

def ask_chatgpt(question: str) -> str:
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API Key found in secrets.toml!")

    client = OpenAI(
        api_key=api_key,
        http_client=httpx.Client(verify=False)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

