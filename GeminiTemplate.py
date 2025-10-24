import streamlit as st
import google.generativeai as genai
from dotenv import dotenv_values

# Load .env keys
config = dotenv_values(".env")

# Configure Gemini
genai.configure(api_key=config["GEMINI_API_KEY"])

# Model setup
model = genai.GenerativeModel("gemini-2.5-pro")

# User input
st.title("Gemini AI Travel Assistant")
user_input = st.text_input("Ask Gemini something:")

if st.button("Generate Response"):
    response = model.generate_content(user_input)
    st.subheader("Response:")
    st.write(response.text)
