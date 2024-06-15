from flask import Flask, request, send_file, render_template, flash, redirect, url_for, session,send_from_directory
from loadUserDataBase import register_user, validate_user
from seg import segment_image
import cv2
import numpy as np
import io
from PIL import Image
from gevent import pywsgi
import argparse
import os

# 创建app项目
app = Flask(__name__)
app.secret_key = 'your_secret_key'


# 加载主页
@app.route('/', methods=['GET'])
def load_website():
    return render_template('app.html')

# 加载图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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


from flask import session, redirect, url_for, flash


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask application.')
    # 默认参数
    parser.add_argument('--mode', choices=['local', 'server'], default='local',
                        help='Running mode: "local" for development (default), "server" for production.')

    args = parser.parse_args()

    if args.mode == 'local':
        print("Running in local development mode...")
        app.run(debug=True)
    elif args.mode == 'server':
        print("Running in production server mode...")
        # 使用gevent的WSGIServer来提高性能
        server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        server.serve_forever()
