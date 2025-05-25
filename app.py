import streamlit as st
import pdfplumber
import requests
import os
import json
import time

st.set_page_config(page_title="📄 UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Analyzer (Chunked PDF)")

API_URL = "https://api.langflow.astra.datastax.com/lf/2eadbc26-1bb9-446f-a787-8c982df90ec8/api/v1/run/f3fd7a6e-7634-4d55-9a49-92c2f9a8e37f"
API_TOKEN = st.secrets["ASTRA_API_TOKEN"] if "ASTRA_API_TOKEN" in st.secrets else os.getenv("ASTRA_API_TOKEN")

def call_langflow(text):
    payload = {
        "input_value": text,
        "output_type": "chat",
        "input_type": "text"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    except Exception as e:
        return f"⚠️ Error with this chunk: {e}"

uploaded_file = st.file_uploader("📥 Upload your UPI PDF statement", type=["pdf"])

if uploaded_file and API_TOKEN:
    st.success("✅ PDF uploaded. Processing...")
    insights = []

    with pdfplumber.open(uploaded_file) as pdf:
        total_pages = len(pdf.pages)
        chunk_size = 2  # You can adjust this to 1–3 pages max

        for start in range(0, total_pages, chunk_size):
            chunk_text = ""
            for i in range(start, min(start + chunk_size, total_pages)):
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    chunk_text += page_text + "\n"

            if chunk_text.strip():
                with st.spinner(f"🔍 Analyzing pages {start + 1}–{min(start + chunk_size, total_pages)}..."):
                    result = call_langflow(chunk_text)
                    insights.append(f"### 📄 Pages {start + 1}–{min(start + chunk_size, total_pages)}\n{result}")
                    time.sleep(1)  # Optional: slight delay between calls to avoid rate limits

    st.subheader("📋 Final Financial Insights")
    for insight in insights:
        st.markdown(insight)
else:
    if not API_TOKEN:
        st.warning("🔐 ASTRA_API_TOKEN missing in secrets.")
