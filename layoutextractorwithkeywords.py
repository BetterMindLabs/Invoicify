import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini Pro
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image, prompt])
    return response.text

# Streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor", layout="wide")
st.header("Multilanguage Invoice Extractor")

# Project showcase description
with st.expander("🎓 About This Project"):
    st.markdown("""
    This **AI-powered Invoice Extractor** is a student-developed innovation that blends real-world utility with modern technology. 
    Built using **Google’s Gemini AI** and **Streamlit**, it intelligently understands and reconstructs invoices—even in **multiple languages** and **handwritten formats**.

    ### 🌟 Key Highlights:
    - ✅ Advanced **keyword extraction** to fetch buyer/seller details, totals, and invoice metadata.
    - 🧠 Accurate **layout detection** to preserve the document structure.
    - 📋 Capable of **extracting complex tables** with proper formatting.
    - 🌐 Supports **multilingual** documents for global use.
    - ✍️ Detects and reads **handwritten content** with impressive accuracy.
    
    This project reflects the **future-ready skills** our students are developing—combining artificial intelligence, programming, and practical problem-solving to build tools that matter in industries like **finance, logistics, retail, and e-commerce**.
    """)

# Input prompt and image upload
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image...", type=['jpg', 'png', 'jpeg', 'webp'])

# Layout split into two columns
col1, col2 = st.columns([1, 2])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Process")

# Markdown structure replication prompt
prompt = (
    "You are an expert in document understanding, specializing in parsing and replicating invoice structures. "
    "Your task is to replicate the entire document sequentially in markdown format, maintaining the original structure "
    "of the document from top to bottom..."
)

# Keyword extraction prompt
key_prompt = (
    "You are an advanced document analysis model with expertise in extracting specific structured data from invoices. "
    "Your task is to carefully analyze the provided invoice and extract the following information accurately..."
)

if submit and uploaded_file is not None:
    try:
        response = get_gemini_response(input_text, image, prompt)
        with col2:
            st.markdown(response, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    try:
        response = get_gemini_response(input_text, image, key_prompt)
        with col2:
            st.markdown(response, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"An error occurred in Keyword data extraction: {e}")
