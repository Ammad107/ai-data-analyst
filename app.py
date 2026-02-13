import streamlit as st
from analyst import load_data, professional_clean, run_agentic_code, get_ai_insight

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 AI Data Analyst")
st.write("Upload a CSV or Excel file to begin your analysis.")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Load and Clean
    df = load_data(uploaded_file)
    df = professional_clean(df)
    
    st.write("### Data Preview", df.head())
    
    query = st.text_input("Ask the AI something about your data:")
    
    if query:
        with st.spinner("Thinking..."):
            # Get AI Text Insight
            summary = df.describe().to_string()
            insight = get_ai_insight(summary, query)
            st.info(f"**AI Insight:** {insight}")
            
            # Get Chart
            result = run_agentic_code(df, query)
            if result["plot"]:
                st.plotly_chart(result["plot"])
