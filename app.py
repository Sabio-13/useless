from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # Get data from form
    url = request.form.get('url')
    logo = request.files.get('logo')
    
    # Validate URL
    if not url:
        return "URL is required", 400
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Add logo if provided
    if logo:
        try:
            logo_img = Image.open(logo.stream)
            
            # Resize logo
            logo_size = min(qr_img.size) // 4
            logo_img = logo_img.resize((logo_size, logo_size))
            
            # Calculate position to center logo
            pos = (
                (qr_img.size[0] - logo_img.size[0]) // 2,
                (qr_img.size[1] - logo_img.size[1]) // 2
            )
            
            # Paste logo on QR code
            qr_img.paste(logo_img, pos)
        except Exception as e:
            print(f"Error processing logo: {e}")
    
    # Save image to bytes
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)