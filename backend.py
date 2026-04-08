from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import io

app = Flask(__name__)
CORS(app)

# ---------------- AI MODEL (OPTIONAL) ----------------
# If you add a trained model later, load here
model = None
classes = ["Acne", "Dry", "Oily"]

def predict_skin(image):
    # If model exists → use it
    if model:
        img = cv2.resize(image, (128, 128))
        img = img / 255.0
        img = np.reshape(img, (1, 128, 128, 3))
        pred = model.predict(img)
        return classes[np.argmax(pred)]

    # Fallback logic (works now)
    brightness = np.mean(image)
    return "Oily" if brightness > 150 else "Dry"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return {"message": "CosmoCare Backend Running 🚀"}


# ---------------- SKIN SCAN ----------------
@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    skin_type = predict_skin(img)

    return jsonify({
        "result": f"Detected: {skin_type}",
        "skin_type": skin_type
    })


# ---------------- INGREDIENT CHECK ----------------
@app.route('/ingredients', methods=['POST'])
def ingredients():
    data = request.json
    ingredient = data.get("ingredient", "")

    if "alcohol" in ingredient.lower():
        result = "⚠️ May irritate skin"
    elif "paraben" in ingredient.lower():
        result = "⚠️ Avoid for sensitive skin"
    else:
        result = "✅ Safe ingredient"

    return jsonify({"result": result})


# ---------------- VIRTUAL TRY-ON ----------------
@app.route('/tryon', methods=['POST'])
def tryon():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Approx lips region
        lip_y1 = int(y + h * 0.65)
        lip_y2 = int(y + h * 0.85)
        lip_x1 = int(x + w * 0.3)
        lip_x2 = int(x + w * 0.7)

        # Apply lipstick (red)
        img[lip_y1:lip_y2, lip_x1:lip_x2] = [0, 0, 255]

    # Convert image to bytes
    _, buffer = cv2.imencode('.jpg', img)

    return send_file(
        io.BytesIO(buffer),
        mimetype='image/jpeg'
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)