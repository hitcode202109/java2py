from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template
from models import db, User, Friend, Post
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


SECRET_KEY = 'your_secret_key'

api = Blueprint('api', __name__)


@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    iduser = data.get('iduser')
    useremail = data.get('useremail')
    password = data.get('password')

    if not all([username, iduser, useremail, password]):
        return jsonify({'message': 'All fields are required'}), 400

    user = User.query.filter_by(useremail=useremail).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.set_password(password)
    user.status = 1  # Assuming 1 means "activated"
    db.session.commit()

    return jsonify({'message': 'User status updated successfully'}), 200


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    iduser = data.get('iduser')
    password = data.get('password')

    # 检查是否提供了iduser和password
    if not iduser or not password:
        return jsonify({'message': 'User ID and password are required'}), 400

    # 查找用户
    user = User.query.filter_by(iduser=iduser).first()

    # 检查用户是否存在以及密码是否正确
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid user ID or password'}), 401

    # 生成JWT令牌
    token = jwt.encode({
        'user_id': user.iduser,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')

    response = jsonify({'token': token})
    response.status_code = 200

    # 将用户ID保存在会话中，以便在重定向后的页面使用
    session['user_id'] = user.iduser

    return jsonify({'message': 'login succeess'}), 200


@api.route('/userfriend', methods=['POST'])
def userfriend():
    user_id = session.get('user_id')
    print(user_id)

    if user_id is None:
        return jsonify({'message': 'User ID not found in session'}), 401

    data = request.get_json()
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({'message': 'Friend ID is required'}), 400

    friend = User.query.get(friend_id)
    if friend is None:
        return jsonify({'message': 'Friend not found'}), 404

    new_friend = Friend(idfriend=user_id, friendid=friend_id)
    db.session.add(new_friend)
    db.session.commit()

    return jsonify({'message': 'Friend added successfully!'}), 200


@api.route('/postopinion', methods=['GET', 'POST'])
def post_opinion():
    if request.method == 'POST':
        user_id = session.get('user_id')

        user_id = 1

        if user_id is None:
            return jsonify({'message': 'User ID not found in session'}), 401

        data = request.get_json()
        content = data.get('content')

        print(content)


        if not content:
            return jsonify({'message': 'Content is required'}), 400

        new_opinion = Post(content=content, userid=user_id)
        db.session.add(new_opinion)
        db.session.commit()

        return jsonify({'message': 'post success, click this button to your home page'}), 200

    return render_template('post_opinion.html')

@api.route('/userhome', methods=['GET'])
def user_home():
    user_id = session.get('user_id')
    user_id = 1  # 这里将 user_id 硬编码为 1，实际应用中应根据会话获取

    if user_id is None:
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示的帖子数量

    # 分页查询，按时间戳降序排列
    pagination = Post.query.filter_by(userid=user_id).order_by(Post.timestamp.desc()).paginate(page, per_page, False)
    posts = pagination.items

    if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        return render_template('partials/_posts.html', posts=posts)

    return render_template('user_home.html', user=User.query.get(user_id), posts=posts, pagination=pagination)
'''
@api.route('/administer', methods=['GET'])
def

# Example of a protected route
@api.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        current_user = User.query.get(data['user_id'])
    except:
        return jsonify({'message': 'Token is invalid'}), 401

    return jsonify({'message': f'Hello, {current_user.name}'})'''''
