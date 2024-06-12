from flask import Flask, request, send_file, render_template, flash, redirect, url_for, session
from loadUserDataBase import register_user, validate_user
from seg import segment_image
import cv2
import numpy as np
import io
from PIL import Image

# 创建app项目
app = Flask(__name__)
app.secret_key = 'your_secret_key'


# 加载主页
@app.route('/', methods=['GET'])
def load_website():
    return render_template('index.html')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = register_user(username, password)

        if user_id:
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')

    return render_template('register.html')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = validate_user(username, password)

        if user:
            session['username'] = username
            return redirect(url_for('load_website'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


# 登出
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('load_website'))


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
