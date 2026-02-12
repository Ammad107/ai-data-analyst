import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import streamlit as st
import io

# --- PERFORMANCE LAYER: Instant Data Loading ---
@st.cache_data(show_spinner=False)
def load_data(uploaded_file):
    """Caches data in memory so it doesn't reload on every click."""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

# --- CLEANING LAYER: The 'Janitor' ---
@st.cache_data(show_spinner=False)
def professional_clean(df: pd.DataFrame):
    """Standardizes columns and handles missing values."""
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # Clean currency and commas
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
            except: continue
    # Fill gaps with median (numeric) or 'Unknown' (text)
    for col in df.columns:
        if df[col].isnull().any():
            if np.issubdtype(df[col].dtype, np.number):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("Unknown")
    return df

# --- EXECUTION LAYER: Agentic Code ---
def run_agentic_code(df: pd.DataFrame, prompt: str):
    local_ns = {"pd": pd, "np": np, "df": df, "px": px, "go": go}
    p = prompt.lower()
    
    # Reasoning logic for chart types
    if "correlation" in p or "heatmap" in p:
        code = "result_plot = px.imshow(df.select_dtypes(include='number').corr(), text_auto=True, color_continuous_scale='RdBu_r')"
    elif "trend" in p or "line" in p:
        num_cols = df.select_dtypes(include='number').columns
        code = f"result_plot = px.line(df, y='{num_cols[0]}', title='Automated Trend Analysis')"
    elif "distribution" in p or "histogram" in p:
        num_cols = df.select_dtypes(include='number').columns
        code = f"result_plot = px.histogram(df, x='{num_cols[0]}', marginal='box')"
    else:
        code = "result_text = df.describe().to_html()"

    try:
        exec(code, {}, local_ns)
        return {"plot": local_ns.get("result_plot"), "text": local_ns.get("result_text")}
    except Exception as e:
        return {"error": str(e)}

def get_ai_insight(summary: str, query: str):
    """Fetches insights from local Ollama."""
    full_prompt = f"Data Summary:\n{summary}\n\nUser Question: {query}\nProvide 3 short, actionable business insights."
    try:
        proc = subprocess.run(["ollama", "run", "llama3.1"], input=full_prompt.encode(), stdout=subprocess.PIPE, timeout=15)
        return proc.stdout.decode()
    except:
        return "Insight generation skipped (check if Ollama is running)."