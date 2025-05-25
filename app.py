import streamlit as st

st.set_page_config(page_title="UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Assistant – Embedded View")
st.markdown(
    """
    Upload your UPI statement and chat with your financial assistant right here.
    This tool will analyze your transactions and suggest personalized insights, budget tips, and saving advice.
    """
)

# Embed Langflow Flow UI
st.components.v1.html(
    """
    <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.7/dist/build/static/js/bundle.min.js"></script>

    <langflow-chat
        window_title="UPI Analysis Assistant"
        flow_id="f3fd7a6e-7634-4d55-9a49-92c2f9a8e37f"
        host_url="https://astra.datastax.com">
    </langflow-chat>
    """,
    height=650,
    scrolling=True,
)
