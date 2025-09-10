import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ---- LOAD API KEY ----
load_dotenv(dotenv_path=".env")  # or key.env if you renamed it
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API key not found. Please set GOOGLE_API_KEY in a .env file or environment variable.")
else:
    genai.configure(api_key=API_KEY)

# ---- PAGE CONFIG ----
st.set_page_config(page_title=" AI-Powered Python Exercise Generator", page_icon="📝", layout="wide")

# ---- CUSTOM STYLES ----
st.markdown(
    """
    <style>
        /* App background & text */
        body {
            background-color: #f0f2f6;
            color: #333333;
            font-family: Arial, Helvetica, sans-serif;
        }

        /* Title */
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
            font-family: Georgia, 'Times New Roman', serif;
        }

        /* Subtitles */
        .subtitle {
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            font-family: Verdana, Geneva, sans-serif;
        }

        /* Text areas */
        .stTextArea textarea {
            border-radius: 8px;
            border: 2px solid #4CAF50;
            padding: 10px;
            font-size: 16px;
            font-family: Courier, monospace;
        }

        /* Button */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            height: 50px;
            font-size: 18px;
            font-family: Tahoma, Geneva, sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- HEADER ----
st.markdown("<h1> 🐍 AI-Powered Python Exercise Generator</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#34495e;'>⚡ Generate customized Python coding exercises instantly with the power of AI</p>",
    unsafe_allow_html=True
)

# ---- INPUT SECTION ----
with st.expander("🔻 Input Parameters", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        topics = st.text_area(
            "Enter Topics (comma-separated):",
            "e.g., Python programming, Data analysis, Machine learning"
        )

        difficulty = st.selectbox(
            "Select Difficulty Level:",
            ["Beginner", "Intermediate", "Advanced"]
        )

    with col2:
        requirements = st.text_area(
            "Enter Additional Requirements:",
            "e.g., Exercises should include code examples, edge cases, explanations"
        )

# ---- GENERATE BUTTON ----
if st.button("Generate Exercises"):
    if not topics or not requirements:
        st.warning("Please enter both topics and requirements.")
    else:
        try:
            # Prepare prompt for generative AI
            prompt = f"""Generate Python programming exercises based on the following topics and requirements:

Topics: {topics}
Difficulty: {difficulty}
Requirements: {requirements}

Please provide detailed exercises, including clear instructions and expected output where applicable.
"""

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            generated_exercises = response.text

            # ---- DISPLAY EXERCISES ----
            with st.expander("📝 Generated Exercises", expanded=True):
                st.markdown(generated_exercises)  # plain text, default Streamlit rendering
                
                st.download_button(
                    label="📥 Download Exercises as Text",
                    data=generated_exercises,
                    file_name="python_exercises.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

