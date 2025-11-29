from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, min=6)
    role = fields.Str(missing='user')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Validate input
        schema = UserSchema()
        data = schema.load(request.json)
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user = User(email=data['email'], role='user')
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,  # Added token to signup
            'user': user.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'error': 'No account found with this email'}), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({'error': 'Incorrect password'}), 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin/signup', methods=['POST'])
def admin_signup():
    try:
        schema = UserSchema()
        data = schema.load(request.json)
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create admin user
        user = User(email=data['email'], role='admin')
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )
        
        return jsonify({
            'message': 'Admin created successfully',
            'access_token': access_token,  # Added token to admin signup
            'user': user.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Find admin user
        user = User.query.filter_by(email=email, role='admin').first()
        
        # Check if admin exists
        if not user:
            return jsonify({'error': 'No admin account found with this email'}), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({'error': 'Incorrect password'}), 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500