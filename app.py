import streamlit as st
import json
from langflow.load import run_flow_from_json  # <- make sure langflow is installed

st.set_page_config(page_title="UPI Financial Analyzer", layout="centered")
st.title("💸 UPI Financial Insights")
st.markdown("Upload your UPI transaction statement (.txt) and get a complete financial breakdown + personalized advice.")

uploaded_file = st.file_uploader("📤 Upload UPI Text File", type=["txt"])

if uploaded_file:
    st.success("✅ File uploaded. Processing...")
    file_content = uploaded_file.read().decode("utf-8")

    # Load Langflow flow
    with open("upi_flow.json", "r") as f:
        flow_json = json.load(f)

    try:
        result = run_flow_from_json(
            flow=flow_json,
            inputs={"text": file_content}
        )
        # Display outputs
        if isinstance(result, dict):
            for k, v in result.items():
                st.subheader(f"📌 {k.capitalize().replace('_', ' ')}")
                if isinstance(v, dict):
                    st.json(v)
                else:
                    st.write(v)
        else:
            st.write(result)
    except Exception as e:
        st.error(f"🚫 Error running flow: {e}")
