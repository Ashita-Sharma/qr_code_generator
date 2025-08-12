import qrcode
from flask import Flask, request, redirect, render_template, flash
import random
import cv2
import string
from PIL import Image
import uuid
import os
print(random.randint(1, 100))
app = Flask(__name__)
app.secret_key = 'your-secret-key'
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/qrcode', methods=['POST'])
def qr_code():
    link = request.form['url']
    name = request.form['image_name']
    os.makedirs("static/gen_qrcodes", exist_ok=True)
    img = qrcode.make(link)
    type(img)  # qrcode.image.pil.PilImage
    img_path = f"static/gen_qrcodes/{name}.png"
    img.save(f"static/gen_qrcodes/{name}.png")
    return render_template("qrcode_generated.html", name=name, link=link)
@app.route('/reader', methods=['POST'])
def code_reader():
    # Check if form exists
    if 'code' not in request.files:
        flash('No file uploaded')
        return redirect('/')
    file = request.files['code']
    #check if file was added
    if file.filename == '':
        flash('No file selected')
        return redirect('/')
#ALL OF THIS IS TEMPORARY
    if file:
        # Save uploaded file temporarily
        temp_filename = f"temp_{uuid.uuid4().hex[:8]}.png"
        #^^^^ creates an 8 chara uuid that is smaller than normal but still unique enough
        temp_path = f"static/temp/{temp_filename}"

        # Create temp folder
        os.makedirs("static/temp", exist_ok=True)
        file.save(temp_path)

        try:

            image = cv2.imread(temp_path)
            detector = cv2.QRCodeDetector()
            decoded_text, points, straight_qrcode = detector.detectAndDecode(image)

            if decoded_text and decoded_text[0]:
                result = {"success": True, "data": decoded_text}
            else:
                result = {"success": False, "error": "No QR code found in image"}
        except Exception as e:
            result = {"success": False, "error": f"Error reading image: {str(e)}"}
        if os.path.exists(temp_path):
            os.remove(temp_path)
            #DONT FORGET TO VArIABLIZE THE VAriABLE
        return render_template("reader.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)