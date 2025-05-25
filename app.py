import streamlit as st
import requests
import pdfplumber
import os
import json

st.set_page_config(page_title="📄 UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Analyzer (PDF Powered)")

API_URL = "https://api.langflow.astra.datastax.com/lf/2eadbc26-1bb9-446f-a787-8c982df90ec8/api/v1/run/f3fd7a6e-7634-4d55-9a49-92c2f9a8e37f"
API_TOKEN = st.secrets["ASTRA_API_TOKEN"] if "ASTRA_API_TOKEN" in st.secrets else os.getenv("ASTRA_API_TOKEN")

uploaded_file = st.file_uploader("📥 Upload your UPI PDF statement", type=["pdf"])

if uploaded_file and API_TOKEN:
    with pdfplumber.open(uploaded_file) as pdf:
        extracted_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
    # Limit input to ~10,000 characters
    extracted_text = extracted_text[:10000]


    st.success("✅ PDF extracted successfully.")

    payload = {
        "input_value": extracted_text,
        "output_type": "chat",
        "input_type": "text"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        with st.spinner("🧠 Analyzing your UPI statement..."):
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            st.subheader("📋 Financial Insights")
            if "text" in data:
                st.markdown(data["text"])
            else:
                st.json(data)

    except Exception as e:
        st.error(f"❌ Error while calling Langflow API:\n\n{e}")
else:
    if not API_TOKEN:
        st.warning("🔐 ASTRA_API_TOKEN is missing in secrets.")
