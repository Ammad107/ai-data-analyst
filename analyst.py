import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from groq import Groq

# --- 1. DATA LOADING LAYER ---
def load_data(file):
    """Safely loads CSV or Excel files."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# --- 2. CLEANING LAYER ---
@st.cache_data
def professional_clean(df):
    """Cleans column names and removes currency symbols."""
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object':
            # 'r' prefix handles the SyntaxWarning for the dollar sign
            df[col] = df[col].replace(r'[\$,]', '', regex=True)
    return df

# --- 3. AI INSIGHTS LAYER ---
def get_ai_insight(summary: str, query: str):
    """Connects to Groq Cloud AI using your Secret Key."""
    try:
        if "GROQ_API_KEY" not in st.secrets:
            return "Error: GROQ_API_KEY missing from Streamlit Secrets."
            
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Data Summary:\n{summary}\n\nQuestion: {query}"}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Brain Error: {str(e)}"

# --- 4. VISUALIZATION LAYER ---
def run_agentic_code(df, query):
    """Generates basic charts based on numerical columns."""
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if num_cols:
        fig = px.histogram(df, x=num_cols[0], title=f"Analysis of {num_cols[0]}")
        return {"plot": fig, "text": None}
    return {"plot": None, "text": "No numeric data found for charting."}

