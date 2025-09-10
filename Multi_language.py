import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ---- LOAD API KEY ----
load_dotenv(dotenv_path=".env")  
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API key not found. Please set GOOGLE_API_KEY in a .env file or environment variable.")
else:
    genai.configure(api_key=API_KEY)

# ---- PAGE CONFIG ----
st.set_page_config(page_title="AI-Powered Coding Exercise Generator", page_icon="💻", layout="wide")

# ---- CUSTOM STYLES ----
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(to right, #e0f7fa, #e1bee7);
        }
        .stButton>button {
            background-color: #6A1B9A;
            color: white;
            border-radius: 10px;
            height: 50px;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- HEADER ----
st.markdown("<h1 style='text-align:center; color:#6A1B9A;'>💻 AI-Powered Coding Exercise Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Generate exercises in multiple programming languages with AI</p>", unsafe_allow_html=True)

# ---- INPUT SECTION ----
with st.expander("📌 Input Parameters", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Choose Programming Language:",
            ["Python", "Java", "C++", "JavaScript", "SQL"]
        )

        difficulty = st.selectbox(
            "Select Difficulty Level:",
            ["Beginner", "Intermediate", "Advanced"]
        )

    with col2:
        topics = st.text_area(
            "Enter Topics (comma-separated):",
            "e.g., loops, functions, OOP"
        )

        requirements = st.text_area(
            "Enter Additional Requirements:",
            "e.g., Include explanations, sample input/output"
        )

# ---- GENERATE BUTTON ----
if st.button("Generate Exercises"):
    if not topics or not requirements:
        st.warning("Please enter both topics and requirements.")
    else:
        try:
            # Prompt for multi-language support
            prompt = f"""
Generate {language} programming exercises based on the following:

Topics: {topics}
Difficulty: {difficulty}
Requirements: {requirements}

Please provide clear problem statements, code examples in {language}, and expected output where applicable.
"""

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            generated_exercises = response.text

            # ---- DISPLAY EXERCISES ----
            with st.expander("📝 Generated Exercises", expanded=True):
                st.markdown(generated_exercises)

                st.download_button(
                    label="📥 Download Exercises as Text",
                    data=generated_exercises,
                    file_name=f"{language.lower()}_exercises.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
