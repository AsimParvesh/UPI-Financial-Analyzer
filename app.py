import streamlit as st
import json
import os

st.set_page_config(page_title="UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Analyzer")

# Upload input
uploaded_file = st.file_uploader("📤 Upload your UPI transaction .txt file", type=["txt"])

# Check if langflow is available
try:
    from langflow.load import run_flow_from_json
    langflow_available = True
except ImportError:
    st.error("❌ Langflow is not installed.")
    langflow_available = False

# Handle file upload
if uploaded_file and langflow_available:
    raw_text = uploaded_file.read().decode("utf-8")

    # Load the Langflow flow file
    if not os.path.exists("upi_flow.json"):
        st.error("❌ upi_flow.json is missing from your repo.")
    else:
        try:
            with open("upi_flow.json", "r") as f:
                flow_json = json.load(f)

            result = run_flow_from_json(flow_json, inputs={"text": raw_text})

            st.subheader("📋 Financial Insights")
            if isinstance(result, dict):
                for key, value in result.items():
                    st.markdown(f"### {key.replace('_', ' ').capitalize()}")
                    if isinstance(value, dict):
                        st.json(value)
                    else:
                        st.write(value)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"⚠️ Something went wrong running the analysis:\n\n{e}")
