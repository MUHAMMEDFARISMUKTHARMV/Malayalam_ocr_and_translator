import os
import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from googletrans import Translator
import clipboard

# Set TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

# Set the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Initialize Google Translate API
translator = Translator()

def main():
    st.title("PDF Text Translator")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Convert UploadedFile to bytes
        pdf_bytes = uploaded_file.read()

        # Convert PDF bytes to images
        images = convert_from_bytes(pdf_bytes)

        # Process each image and perform multilingual OCR and translation
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='mal+eng', config='--psm 6 --oem 1')
            translated_text = translator.translate(text, src='ml', dest='en').text

            # Use st.expander to dynamically display content for each page
            with st.expander(f"Page {i + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Original Text:")
                    st.write(text)
                    if st.button(f"Copy original text of page {i+1}"):  # Use unique key for each button
                        clipboard.copy(text)

                with col2:
                    st.subheader("Translated Text:")
                    st.write(translated_text)
                    if st.button(f"Copy translated text of page {i+1}"):  # Use unique key for each button
                        clipboard.copy(translated_text)

if __name__ == "__main__":
    main()
