from flask import Flask, request, send_file, render_template, flash, redirect, url_for, session, send_from_directory
from model.loadUserDataBase import register_user, validate_user
from model.seg import segment_image
import cv2
import numpy as np
import io
from PIL import Image
from model.recordUserInfo import InfoRecord
import yaml

with open('config/route.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 创建app项目并设置secret_key
app = Flask(__name__)
app.secret_key = config['app_settings']['secret_key']


# 加载主页
@app.route('/', methods=['GET'])
def load_website():
    return render_template('app.html')


# 加载用户头像
@app.route('/user_avatar', methods=['GET'])
def user_avatar():
    return send_from_directory('static', 'user_avatar.jpg')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user_id = register_user(username, password)
            if user_id:
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An unexpected error occurred during registration. Please try again.', 'danger')
        except ValueError as e:  # 捕获register_user中抛出的ValueError
            flash(str(e), 'warning')  # 将错误信息闪现给用户

    return render_template('register.html')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user = validate_user(username, password)
            if user:
                # 登录成功，将用户名和id存储到session中
                session['username'] = username
                flash('Login successful. Redirecting...', 'success')
                return redirect(url_for('load_website'))
            else:
                raise ValueError('Invalid username or password.')  # 显式抛出错误以便被捕获并闪现给用户
        except ValueError as e:
            flash(str(e), 'danger')  # 显示登录失败的具体原因

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
    username = session.get('username')  # 安全地获取用户ID，避免KeyError
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    mask = segment_image(image)
    mask_image = Image.fromarray(mask)
    byte_io = io.BytesIO()
    mask_image.save(byte_io, 'PNG')
    byte_io.seek(0)


    # 使用InfoRecord类记录图像信息到数据库
    try:
        info_record = InfoRecord(username, image, mask_image)
    except ValueError as e:
        return str(e), 400  # 如果找不到用户，则返回错误信息

    return send_file(byte_io, mimetype='image/png')


# 诊断页面
@app.route('/segmentPage', methods=['GET'])
def segmentPage():
    # 检查用户是否已登录，例如通过验证session中的用户名是否存在
    if 'username' not in session:
        # 如果用户未登录，则重定向到登录页面
        flash('请先登录以访问此页面。')
        return redirect(url_for('login'))  # 假设'login'是您的登录页面路由
    else:
        # 用户已登录，渲染并返回'segmentPage'或相关页面
        return render_template('index.html')  # 注意：这里假设您希望渲染的是'segmentPage.html'而不是'index.html'
