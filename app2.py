from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import io
import datetime

app = Flask(__name__)
CORS(app)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return {"message": "CosmoCare Pro Running 🚀"}


# ---------------- SKIN SCAN ----------------
@app.route('/scan', methods=['POST'])
def scan():
    file = request.files['image']

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    brightness = np.mean(img)

    if brightness > 150:
        skin_type = "Oily"
        recommendation = "Use oil-free products"
    else:
        skin_type = "Dry"
        recommendation = "Use hydrating creams"

    return jsonify({
        "skin_type": skin_type,
        "recommendation": recommendation
    })


# ---------------- PRODUCT SCAN ----------------
@app.route('/product-scan', methods=['POST'])
def product_scan():
    return jsonify({
        "product": "Sample Face Cream",
        "brand": "DemoBrand",
        "authenticity": "Looks Original ✅",
        "ingredients": "No harmful chemicals detected"
    })


# ---------------- INGREDIENT CHECK ----------------
@app.route('/ingredients', methods=['POST'])
def ingredients():
    data = request.json
    ingredient = data.get("ingredient", "")

    if "alcohol" in ingredient.lower():
        result = "⚠️ Harmful"
    else:
        result = "✅ Safe"

    return jsonify({"result": result})


# ---------------- BEAUTY LOOK SCANNER ----------------
@app.route('/beauty-scan', methods=['POST'])
def beauty_scan():
    return jsonify({
        "look": "Natural Glow",
        "suggested_products": [
            "Lakme Foundation",
            "Maybelline Lipstick"
        ]
    })


# ---------------- DOCTOR BOOKING ----------------
appointments = []

@app.route('/book', methods=['POST'])
def book():
    data = request.json

    appointment = {
        "name": data.get("name"),
        "doctor": data.get("doctor"),
        "time": data.get("time"),
        "date": str(datetime.date.today())
    }

    appointments.append(appointment)

    return jsonify({
        "message": "Appointment booked ✅",
        "details": appointment
    })


# ---------------- VIEW APPOINTMENTS ----------------
@app.route('/appointments', methods=['GET'])
def view_appointments():
    return jsonify(appointments)


# ---------------- MEDICATION REMINDER ----------------
reminders = []

@app.route('/reminder', methods=['POST'])
def reminder():
    data = request.json

    reminders.append(data)

    return jsonify({"message": "Reminder added ⏰"})


# ---------------- MEDICAL HISTORY ----------------
@app.route('/history', methods=['GET'])
def history():
    return jsonify({
        "reports": ["Blood Test", "Skin Analysis"],
        "prescriptions": ["Vitamin C", "Moisturizer"]
    })


# ---------------- EMERGENCY ----------------
@app.route('/emergency', methods=['GET'])
def emergency():
    return jsonify({
        "message": "Emergency Alert Sent 🚨",
        "location": "User location shared"
    })


# ---------------- TRY-ON ----------------
@app.route('/tryon', methods=['POST'])
def tryon():
    file = request.files['image']

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        lip_y1 = int(y + h * 0.65)
        lip_y2 = int(y + h * 0.85)
        lip_x1 = int(x + w * 0.3)
        lip_x2 = int(x + w * 0.7)

        img[lip_y1:lip_y2, lip_x1:lip_x2] = [0, 0, 255]

    _, buffer = cv2.imencode('.jpg', img)

    return send_file(io.BytesIO(buffer), mimetype='image/jpeg')


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)