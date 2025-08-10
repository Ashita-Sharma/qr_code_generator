import qrcode, PIL
from flask import Flask, request, redirect, render_template
import random
import string
import os
app = Flask(__name__)
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


if __name__ == '__main__':
    app.run(debug=True)