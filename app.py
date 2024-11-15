from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")  # 密钥从环境变量获取

# 预设密码
PASSWORD = "1234"

# 读取 link.json 文件
def load_collections_from_json():
    try:
        with open("link.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # 如果文件不存在，返回空字典

# 保存数据到 link.json 文件
def save_collections_to_json(collections):
    with open("link.json", 'w') as f:
        json.dump(collections, f, indent=4)

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True  # 设置会话标记
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="密码错误")

    return render_template('login.html')

# 收藏夹管理界面
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # 如果未登录，跳转到登录页面
    
    collections = load_collections_from_json()
    return render_template('dashboard.html', collections=collections)

# 处理添加订阅的表单提交
@app.route('/add_link', methods=['POST'])
def add_link():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # 如果未登录，跳转到登录页面
    
    category = request.form['category']
    link = request.form['link']
    note = request.form['note']

    # 读取现有的收藏夹数据
    collections = load_collections_from_json()

    # 如果分类不存在，创建新的分类
    if category not in collections:
        collections[category] = []

    # 添加新链接到分类中
    collections[category].append({'link': link, 'note': note})

    # 保存更新后的数据到 link.json
    save_collections_to_json(collections)

    # 重定向回收藏夹页面，显示更新后的数据
    return redirect(url_for('dashboard'))

# 登出功能
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # 移除登录标记
    return redirect(url_for('login'))  # 跳转到登录页面

if __name__ == '__main__':
    app.run(debug=True)
