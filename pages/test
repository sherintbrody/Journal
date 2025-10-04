import streamlit as st

st.title("🔍 Secrets Diagnostic")

try:
    token = st.secrets["NOTION_TOKEN"]
    db_id = st.secrets["NOTION_DB_ID"]
    st.success("Secrets loaded successfully.")
    st.write("Token prefix:", token[:10] + "...")
    st.write("Database ID:", db_id)
except Exception as e:
    st.error("Failed to load secrets.")
    st.write(e)
