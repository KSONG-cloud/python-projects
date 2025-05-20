from app.utils.file_processor import process_file
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



@main.route('/')
def index():
    return render_template('upload.html')


# Handles upload POST request
@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part in request")
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)
    

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # Sanitizes a file name 
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        excel_path = process_file(filepath)

        if excel_path:
            return send_file(excel_path, as_attachment=True)
        else:
            return "Failed to process the file.", 500
        
    else:
        return "Invalid file type", 400
    

    


    
