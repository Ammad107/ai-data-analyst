import streamlit as st
from analyst import load_data, professional_clean, run_agentic_code, get_ai_insight

st.set_page_config(page_title="Human-Fast AI Analyst", layout="wide", page_icon="⚡")

# --- INITIALIZE MEMORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

st.title("⚡ Human-Fast AI Analyst")

# Sidebar: Control Panel & History
with st.sidebar:
    st.header("📜 History")
    for msg in st.session_state.chat_history[-5:]:
        st.write(f"- {msg}")
    st.divider()
    if st.button("🗑️ Clear Memory"):
        st.session_state.chat_history = []
        st.rerun()

uploaded = st.file_uploader("Upload Data", type=["csv", "xlsx"])

if uploaded:
    # 1. Instant Load & Clean
    if st.session_state.cleaned_df is None:
        raw_df = load_data(uploaded)
        st.session_state.cleaned_df = professional_clean(raw_df)
    
    df = st.session_state.cleaned_df
    st.success(f"Analyst ready. Processed {len(df)} rows.")

    # 2. Fragmented Interaction (Only this block reruns when typing)
    @st.fragment
    def analysis_zone():
        query = st.text_input("What insight are you looking for?", placeholder="e.g. show correlation heatmap")
        if st.button("🚀 Execute Analysis"):
            st.session_state.chat_history.append(query)
            
            with st.spinner("Processing..."):
                res = run_agentic_code(df, query)
                
                if "error" in res:
                    st.error(f"Robot Error: {res['error']}")
                else:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if res["plot"]: st.plotly_chart(res["plot"], use_container_width=True)
                        if res["text"]: st.write(res["text"], unsafe_allow_html=True)
                    with col2:
                        st.subheader("💡 Robot Insights")
                        insights = get_ai_insight(df.head(5).to_string(), query)
                        st.info(insights)

    analysis_zone()

    # 3. Export Data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Cleaned Dataset", data=csv, file_name="ai_analyst_export.csv")