from flask import Flask, request, send_file, render_template
import numpy as np
import cv2
from seg import segment_image
import io
from PIL import Image

# 创建app项目
app = Flask(__name__)


# 加载主页
@app.route('/', methods=['GET'])
def load_website():
    return render_template('index.html')


# 诊断的按钮事件
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

if __name__ == '__main__':
    app.run(debug=True)