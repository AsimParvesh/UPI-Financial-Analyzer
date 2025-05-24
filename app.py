import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="UPI Analyzer")
st.title("📊 UPI Financial Analyzer (Hosted via Langflow API)")

API_URL = "https://api.langflow.astra.datastax.com/lf/2eadbc26-1bb9-446f-a787-8c982df90ec8/api/v1/run/f3fd7a6e-7634-4d55-9a49-92c2f9a8e37f"
API_TOKEN = st.secrets["ASTRA_API_TOKEN"] if "ASTRA_API_TOKEN" in st.secrets else os.getenv("ASTRA_API_TOKEN")

uploaded_file = st.file_uploader("Upload your UPI .txt file", type=["txt"])

if uploaded_file and API_TOKEN:
    raw_text = uploaded_file.read().decode("utf-8")

    payload = {
        "input_value": raw_text,
        "output_type": "chat",
        "input_type": "text"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        with st.spinner("🔍 Analyzing your UPI statement..."):
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            st.success("✅ Analysis Complete")
            if "text" in data:
                st.markdown(data["text"])
            else:
                st.write(data)
    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    if not API_TOKEN:
        st.warning("🔑 ASTRA_API_TOKEN not set. Add it to Streamlit secrets or as an env variable.")
