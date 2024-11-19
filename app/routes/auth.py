from flask import jsonify, request, Blueprint
from app import app, db
from app.models import User
from app.utils import generate_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token})

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not name:
        return jsonify({'message': 'Name is required'}), 400
    
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    if not password:
        return jsonify({'message': 'Password is required'}), 400

    user = User(name=name, email=email, password=password)
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already in use'}), 400
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})