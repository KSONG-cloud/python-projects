import os
import pytesseract
from .pdf_parser import extract_text_from_pdf
from .ocr import extract_text_from_image
from .excel_writer import save_to_excel
from .parser import parse_statement_text


# For Windows: Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_file(filepath):
    filename, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.pdf':
        text_data = extract_text_from_pdf(filepath)

        # If that fails or returns little text, fall back to OCR
        if not text_data.strip() or len(text_data) < 50:
            text_data = extract_text_from_image(filepath)

        print("TEXT DATA START >>>")
        print(text_data)
        print("<<< TEXT DATA END")

    elif ext in ['.png', '.jpg', '.jpeg']:
        text_data = extract_text_from_image(filepath)
    else:
            return None # Unsupported type
    
    # Parse data into structured data
    structured_data = parse_statement_text(text_data)


    # Create Excel
    excel_path = filename + '.xlsx'
    save_to_excel(structured_data, excel_path)

    return excel_path