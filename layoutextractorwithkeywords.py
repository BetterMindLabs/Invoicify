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

# Input prompt and image upload
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image...", type=['jpg', 'png', 'jpeg', 'webp'])

# Layout split into two columns
col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)
    with col1:  # Image on the left
        st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Process")

# Prompt for the model
prompt = (
    "You are an expert in document understanding, specializing in parsing and replicating invoice structures. "
    "Your task is to replicate the entire document sequentially in markdown format, maintaining the original structure "
    "of the document from top to bottom. This includes:\n\n"
    "- Extracting and replicating all text content as plain text in the markdown output.\n"
    "- Detecting and reproducing all tables in markdown table format exactly as they appear in the original document, "
    "with rows and columns maintained accurately.\n"
    "- Preserving any headings, subheadings, labels, and other text placement as close as possible to the original layout.\n"
    "- Ensuring the final markdown representation is an accurate, sequential reconstruction of the document without omitting any parts.\n\n"
    "Important notes:\n"
    "- Do not add any extra commentary or interpretation to the output.\n"
    "- The output should only contain the replicated content of the document in markdown format, structured as described.\n"
    "- For tables, ensure the alignment and data integrity are preserved while converting them to markdown table syntax.\n"
    "- Maintain text placement, such as line breaks, paragraphs, and indentation, as close as possible to the original document.\n"
)

# prompt for keyword extraction

key_prompt = (
    "You are an advanced document analysis model with expertise in extracting specific structured data from invoices. "
    "Your task is to carefully analyze the provided invoice and extract the following information accurately. "
    "Ensure the extracted values are precise and directly correspond to the data present in the document. "
    "Return the results in a JSON format, where each key corresponds to the field name, and the value is the extracted data. "
    "If any field is not present in the invoice, return the value as 'Not Found'. Here are the fields to extract:\n\n"
    "- invoice_number: The invoice number present on the document.\n"
    "- invoice_date: The date of the invoice.\n"
    "- po_number: The purchase order number associated with the invoice.\n"
    "- total_invoice_amount: The total amount mentioned on the invoice.\n"
    "- total_tax: The total tax amount specified in the invoice.\n"
    "- buyer_name: The name of the buyer.\n"
    "- buyer_email: The email address of the buyer.\n"
    "- buyer_phone: The phone number of the buyer.\n"
    "- buyer_address: The address of the buyer.\n"
    "- buyer_vat_number: The VAT number of the buyer.\n"
    "- seller_name: The name of the seller.\n"
    "- seller_email: The email address of the seller.\n"
    "- seller_phone: The phone number of the seller.\n"
    "- seller_address: The address of the seller.\n"
    "- net_d: The net terms (e.g., Net 30, Net 60) specified on the invoice.\n"
    "- payment_due_date: The date by which payment is due as per the invoice.\n\n"
    "Important guidelines:\n"
    "- Extract the values exactly as they appear in the document.\n"
    "- Ensure all fields are extracted in the correct format (e.g., dates in 'YYYY-MM-DD' format, numbers in decimal format).\n"
    "- Ignore any additional information not explicitly requested in the field list.\n"
    "- Maintain the structure and formatting of the extracted information accurately.\n"
    "- Return the output strictly as a JSON object without any additional commentary or metadata."
)


if submit and uploaded_file is not None:
    try:
        # Call the Gemini model
        response = get_gemini_response(input_text, image, prompt)
        with col2:  # Markdown response on the right
            st.markdown(response, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    try:
        # Call the Gemini model
        response = get_gemini_response(input_text, image, key_prompt)
        with col2:  # Markdown response on the right
            st.markdown(response, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"An error occurred in Keyword data extraction: {e}")