function predict() {
    const formData = new FormData();
    const file = document.getElementById('imageInput').files[0];
    if (!file) {
        alert("Please select an image.");
        return;
    }

    formData.append('file', file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('date').textContent = data.date;
        document.getElementById('time').textContent = data.time;
        document.getElementById('prediction').textContent = data.prediction;
        document.getElementById('instruction').textContent = data.instruction;
        document.getElementById('resultContainer').style.display = 'block';
        // Hiển thị ảnh khoanh vùng ngay trên image preview
        const previewImg = document.getElementById('imagePreview');
        previewImg.src = 'data:image/jpeg;base64,' + data.boxed_image;
        previewImg.style.display = 'block';
    })
    .catch(error => {
        console.error('Prediction failed:', error);
        alert("An error occurred while predicting.");
    });
}

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    predict();
});
