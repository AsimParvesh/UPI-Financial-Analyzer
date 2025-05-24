import streamlit as st
import json
import os

# Try to import run_flow_from_json safely
try:
    from langflow.load import run_flow_from_json
except ImportError:
    st.error("❌ Langflow is not installed or available.")
    st.stop()

st.set_page_config(page_title="UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Analyzer")
st.markdown("Upload a UPI .txt file and get a complete financial breakdown.")

uploaded_file = st.file_uploader("Upload UPI transaction .txt file", type=["txt"])

if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")

    # Load Langflow flow
    if not os.path.exists("upi_flow.json"):
        st.error("❌ upi_flow.json file not found.")
        st.stop()

    with open("upi_flow.json") as f:
        flow = json.load(f)

    try:
        result = run_flow_from_json(flow, inputs={"text": raw_text})
    except Exception as e:
        st.error(f"❌ Error running Langflow flow: {e}")
        st.stop()

    st.subheader("📋 Analysis Result")
    if isinstance(result, dict):
        for k, v in result.items():
            st.markdown(f"### {k.replace('_', ' ').capitalize()}")
            if isinstance(v, dict):
                st.json(v)
            else:
                st.write(v)
    else:
        st.write(result)
