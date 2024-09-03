import os
from flask import Flask, request, send_file
from PIL import Image
import pdf2image
import io

def pdf_to_image(request):
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return 'No selected file', 400
    
    if file and file.filename.lower().endswith('.pdf'):
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(file.read())
        
        # Get the first page
        first_page = images[0]
        
        # Save the image to a bytes buffer
        img_buffer = io.BytesIO()
        first_page.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return send_file(img_buffer, mimetype='image/png')
    else:
        return 'Invalid file format. Please upload a PDF.', 400