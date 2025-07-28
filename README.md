# Lettuce NPK Deficiency Detector

Ứng dụng web sử dụng Deep Learning để nhận diện tình trạng thiếu chất dinh dưỡng (NPK) trên lá xà lách từ ảnh. Người dùng có thể tải ảnh lá lên, hệ thống sẽ xử lý và dự đoán loại thiếu chất (hoặc lá khỏe mạnh) dựa trên mô hình đã huấn luyện.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Thông tin mô hình](#thông-tin-mô-hình)
- [Ghi chú](#ghi-chú)

---

## Giới thiệu

Dự án xây dựng hệ thống nhận diện thiếu chất NPK trên lá xà lách dựa trên ảnh, sử dụng mô hình deep learning (PyTorch). Ứng dụng web phát triển bằng Flask, giao diện đơn giản, dễ sử dụng.

---

## Tính năng

- Nhận diện 4 lớp: Thiếu Nitơ (N), Thiếu Lân (P), Thiếu Kali (K), Lá khỏe mạnh.
- Tiền xử lý ảnh tự động.
- Hiển thị ảnh preview và kết quả dự đoán.
- Giao diện web thân thiện, dễ thao tác.

---

## Cài đặt

### 1. Yêu cầu hệ thống

- Python 3.7+
- pip
- Docker (nếu muốn chạy bằng container)

### 2. Cài đặt thư viện

Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 3. Chuẩn bị mô hình

Đảm bảo file `fasterrcnn_kpn_model.pth` đã có trong thư mục gốc dự án. (https://drive.google.com/drive/u/0/folders/1pJHmDSNsKzqDg0BzaGvNRXG-VPVOlDxf)

### 4. Chạy ứng dụng

Chạy ứng dụng Flask:

```bash
python app.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

### 5. Chạy bằng Docker (tuỳ chọn)

```bash
docker build -t lettuce-npk-detector .
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads lettuce-npk-detector
```

---

## Cách sử dụng

1. Truy cập trang web.
2. Nhấn "Select an image file" để chọn ảnh lá xà lách từ máy tính.
3. Xem ảnh preview.
4. Nhấn "Predict" để nhận kết quả dự đoán.
5. Nhấn "Reset" để làm mới giao diện.

---

## Cấu trúc dự án

```
.
├── app.py
├── fasterrcnn_kpn_model.pth
├── requirements.txt
├── Dockerfile
├── uploads/
├── static/
│   ├── reset.js
│   ├── server.js
│   └── style.css
├── templates/
│   └── index.html
└── README.md
```

- `app.py`: Flask app chạy local.
- `fasterrcnn_kpn_model.pth`: File trọng số mô hình đã huấn luyện.
- `requirements.txt`: Danh sách thư viện cần cài đặt.
- `Dockerfile`: Định nghĩa môi trường Docker.
- `static/`: Chứa file CSS và JS cho giao diện.
- `templates/index.html`: Giao diện chính.

---

## Thông tin mô hình

- Mô hình sử dụng Faster R-CNN (PyTorch) với 4 lớp đầu ra.
- Ảnh được tự động chuyển đổi sang tensor trước khi đưa vào mô hình.
- Tiền xử lý sử dụng torchvision.

---

## Ghi chú

- Thư mục `uploads/` sẽ được tạo tự động nếu chưa tồn tại.
- Đảm bảo file mô hình `.pth` đúng tên và đúng vị trí.
- Nếu chạy bằng Docker, mount thư mục `uploads` để lưu ảnh upload.
- File `static/server.js` có thể không cần thiết cho luồng hiện tại.

