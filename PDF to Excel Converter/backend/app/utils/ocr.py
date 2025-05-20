import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os



def extract_text_from_image(filepath):
    try:
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        
        if ext == '.pdf':
            images = convert_from_path(filepath)
            text = ''
            for image in images:
                text += pytesseract.image_to_string(image)
            return text.strip()
        else:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""