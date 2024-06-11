from flask import Flask, request, send_file, render_template
import numpy as np
import cv2
from model.unet_model import UNet
import torch
import io
from PIL import Image

app = Flask(__name__)

# 加载模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = UNet(n_channels=3, n_classes=1)
net.to(device)
net.load_state_dict(torch.load('best_model.pth', map_location=device))
net.eval()

# 图像分割函数
def segment_image(image):
    origin_shape = image.shape[:2]  # 原始图像形状
    image = cv2.resize(image, (256, 256))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.transpose((2, 0, 1))
    image = image / 255.0
    image_tensor = torch.from_numpy(image).unsqueeze(0).to(device=device, dtype=torch.float32)

    # 模型推理
    with torch.no_grad():
        pred = net(image_tensor)
        pred = torch.sigmoid(pred)
        pred = pred.squeeze().cpu().numpy()
        pred[pred >= 0.5] = 255
        pred[pred < 0.5] = 0
        pred = pred.astype(np.uint8)

    # 恢复到原始分辨率
    pred = cv2.resize(pred, (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_NEAREST)
    return pred

# 接收图像并进行分割
@app.route('/segment', methods=['POST'])
def segment():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    mask = segment_image(image)
    mask_image = Image.fromarray(mask)
    byte_io = io.BytesIO()
    mask_image.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

# 加载网页
@app.route('/', methods=['GET'])
def load_website():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)