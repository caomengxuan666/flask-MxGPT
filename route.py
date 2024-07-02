import time

from flask import Flask, request, send_file, render_template, flash, redirect, url_for, session, send_from_directory, \
    jsonify
from model.loadUserDataBase import register_user, validate_userbyname, validate_userbyemail
from model.seg import segment_image
import cv2
import numpy as np
import io
from PIL import Image
from model.recordUserInfo import InfoRecord
from model.static_DR_Enhance import ImageEnhancer  # 确保从正确的路径导入ImageEnhancer类
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
    return send_from_directory('static', 'img/avatar/default_user_avatar.jpg')


# 登出
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('load_website'))


# 登录


@app.route('/reg_log', methods=['GET', 'POST'])
def reg_or_login():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'register':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            try:
                user_id = register_user(username, email, password)
                if user_id:
                    return jsonify({"success": True, "message": "Registration successful. Please login."}), 200
                else:
                    return jsonify({"success": False,
                                    "message": "An unexpected error occurred during registration. Please try again."}), 400
            except ValueError as e:
                return jsonify({"success": False, "message": str(e)}), 400

        elif action == 'login':
            email = request.form['email']
            password = request.form['password']
            try:
                user = validate_userbyemail(email, password)
                if user:
                    # 登录成功，将用户信息存储到session中
                    # session['email'] = email
                    session['username'] = user[1]
                    return jsonify({"success": True, "message": "Login successful. Redirecting..."})
                else:
                    return jsonify({"success": False, "message": "Invalid username or password."}), 401
            except ValueError as e:
                return jsonify({"success": False, "message": str(e)}), 400

        else:
            return jsonify({"success": False, "message": "Invalid action selected."}), 400

    # GET请求或表单提交无效时，返回带有注册和登录选项的页面
    return render_template('reg_log.html')


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


# 医学影像分割页面
@app.route('/segmentPage', methods=['GET'])
def segmentPage():
    # 检查用户是否已登录，例如通过验证session中的用户名是否存在
    if 'username' not in session:
        # 如果用户未登录，则重定向到登录页面
        flash('请先登录以访问此页面。')
        return redirect(url_for('reg_or_login'))
    else:
        # 用户已登录，渲染并返回'segmentPage'或相关页面
        return render_template('SegmentPage.html')  # 注意：这里假设您希望渲染的是'segmentPage.html'而不是'SegmentPage.html'

# 医学影像增强界面
@app.route('/DR_enhancePage', methods=['GET'])
def DR_enhancePage():
    # 检查用户是否已登录，例如通过验证session中的用户名是否存在
    if 'username' not in session:
        # 如果用户未登录，则重定向到登录页面
        flash('请先登录以访问此页面。')
        return redirect(url_for('reg_or_login'))
    else:
        # 用户已登录，渲染并返回'enhancePage'或相关页面
        return render_template('enhancePage.html')

@app.route('/DR_enhance', methods=['POST'])
def DR_enhance():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    username = session.get('username')  # 注意确保在实际应用中已设置session

    # 读取并解码图像
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # 实例化ImageEnhancer并进行图像处理
    image_enhancer = ImageEnhancer(image=image)  # 假设ImageEnhancer接受字节数据
    processed_image = image_enhancer.enhance_image()  # 或者是其他处理方法

    # 将OpenCV图像转换为PIL图像以便保存到BytesIO
    pil_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(pil_image)

    # 创建BytesIO对象并保存图像
    byte_io = io.BytesIO()
    pil_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    # 等待三秒
    time.sleep(3)

    return send_file(byte_io, mimetype='image/png')