from flask import Flask, request, render_template, jsonify # type: ignore
import torch # pyright: ignore[reportMissingImports]
from torchvision.models.detection import fasterrcnn_resnet50_fpn # type: ignore
from torchvision import transforms # type: ignore
from PIL import Image, ImageDraw, ImageFont # type: ignore
import os
from werkzeug.utils import secure_filename # type: ignore
from datetime import datetime
import base64
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class_names = {
    1: "Thiếu Nitơ (N)",
    2: "Thiếu Lân (P)",
    3: "Thiếu Kali (K)",
    4: "Lá khỏe mạnh"
}

instructions = {
    "Thiếu Nitơ (N)": "Bón thêm phân đạm (ure, amoni nitrat).",
    "Thiếu Lân (P)": "Bón thêm phân lân (DAP, super lân).",
    "Thiếu Kali (K)": "Bón thêm phân kali (KCl, K2SO4).",
    "Lá khỏe mạnh": "Không cần can thiệp, cây đang phát triển tốt."
}

# Fix deprecation warning: use 'weights=None' instead of 'pretrained=False'
model = fasterrcnn_resnet50_fpn(weights=None, num_classes=5)
model.load_state_dict(torch.load("fasterrcnn_kpn_model.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([transforms.ToTensor()])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image = Image.open(filepath).convert("RGB")
        img_tensor = transform(image)

        with torch.no_grad():
            prediction = model([img_tensor])[0]

        labels = prediction['labels']
        scores = prediction['scores']
        boxes = prediction['boxes']

        threshold = 0.2  # Giảm threshold để nhận diện nhạy hơn
        label_name = "Không xác định"
        recommendation = "Không rõ biện pháp."
        best_score = 0
        best_label = None

        # Vẽ tất cả bounding box có score đủ lớn và không phải lá khỏe mạnh
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()

        found = False
        for box, label, score in zip(boxes, labels, scores):
            name = class_names.get(label.item(), "Unknown")
            if name == "Lá khỏe mạnh":
                continue  # Bỏ qua vùng lá khỏe mạnh
            if score >= threshold:
                found = True
                box = [int(x) for x in box]
                draw.rectangle(box, outline="red", width=3)
                draw.text((box[0], box[1]), f"{name}: {score:.2f}", fill="yellow", font=font)
                if score > best_score:
                    best_score = score
                    best_label = label

        # Nếu không tìm thấy vùng bệnh nào, kiểm tra có vùng "Lá khỏe mạnh" không
        if found and best_label is not None:
            label_id = best_label.item()
            label_name = class_names.get(label_id, label_name)
            recommendation = instructions.get(label_name, recommendation)
        else:
            # Nếu có ít nhất 1 vùng "Lá khỏe mạnh" vượt threshold thì trả về "Lá khỏe mạnh"
            healthy_found = any(
                class_names.get(label.item(), "Unknown") == "Lá khỏe mạnh" and score >= threshold
                for label, score in zip(labels, scores)
            )
            if healthy_found:
                label_name = "Lá khỏe mạnh"
                recommendation = instructions.get(label_name, "Không rõ biện pháp.")
            else:
                label_name = "Không xác định"
                recommendation = "Không rõ biện pháp."

        # Chuyển ảnh đã vẽ box sang base64 để trả về frontend
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        now = datetime.now()
        return jsonify({
            "prediction": label_name,
            "instruction": recommendation,
            "date": now.strftime("%Y/%m/%d"),
            "time": now.strftime("%H:%M:%S"),
            "boxed_image": img_str
        })
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
