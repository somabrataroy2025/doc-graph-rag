import streamlit as st

file = st.file_uploader("pick a file",type=["pdf"])
if file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")