import pdfplumber




def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or '' # '' is for safely handling None
            text += "\n\n"
    return text.strip()