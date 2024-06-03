from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(
       version=1,  # Adjust the version as needed
        box_size=8,  # Adjust the box size for medium QR code
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

@app.route('/')
def index():
    return render_template('index.html', qr_code_data=None)

@app.route('/generate', methods=['POST'])
def generate():
    data_input = request.form['data']
    img = generate_qr_code(data_input)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    qr_code_data = 'data:image/png;base64,' + img_base64
    return render_template('index.html', qr_code_data=qr_code_data)

if __name__ == '__main__':
    app.run(debug=True)
