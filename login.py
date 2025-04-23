import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

st.title("The Joins Login")
st.text_input("Username Here")
st.text_input("Password Here")

st.button("Login")