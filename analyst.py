import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from groq import Groq

# --- CLEANING LAYER ---
@st.cache_data
def professional_clean(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object':
            # Raw string 'r' handles the syntax warning
            df[col] = df[col].replace(r'[\$,]', '', regex=True)
    return df

# --- AI INSIGHTS ---
def get_ai_insight(summary: str, query: str):
    try:
        # Looks for the key in your Streamlit Advanced Settings
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Data Summary:\n{summary}\n\nQuestion: {query}"}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Brain Error: {str(e)}"

# --- EXECUTION LAYER ---
def run_agentic_code(df, query):
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) > 0:
        fig = px.histogram(df, x=num_cols[0], title=f"Analysis of {num_cols[0]}")
        return {"plot": fig, "text": None}
    return {"plot": None, "text": "No numeric data found."}
