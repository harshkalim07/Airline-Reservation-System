from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from marshmallow import ValidationError
from app.schemas.user_schema import UserRegistrationSchema, UserLoginSchema

class AuthController:
    """Controller for handling authentication logic"""
    
    @staticmethod
    def register_user(data):
        """
        Register a new user
        Args:
            data: Dictionary containing email, password, and optional role
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            # Validate input
            schema = UserRegistrationSchema()
            validated_data = schema.load(data)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=validated_data['email']).first()
            if existing_user:
                return {'error': 'Email already registered'}, 400
            
            # Create new user
            user = User(
                email=validated_data['email'],
                role=validated_data.get('role', 'user')
            )
            user.set_password(validated_data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Generate access token
            access_token = create_access_token(
                identity=user.id,
                additional_claims={'role': user.role},
                expires_delta=timedelta(hours=24)
            )
            
            return {
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'access_token': access_token
            }, 201
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Registration failed: {str(e)}'}, 500
    
    @staticmethod
    def login_user(data):
        """
        Authenticate user and generate JWT token
        Args:
            data: Dictionary containing email and password
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            # Validate input
            schema = UserLoginSchema()
            validated_data = schema.load(data)
            
            # Find user
            user = User.query.filter_by(email=validated_data['email']).first()
            
            if not user or not user.check_password(validated_data['password']):
                return {'error': 'Invalid email or password'}, 401
            
            # Generate tokens
            access_token = create_access_token(
                identity=user.id,
                additional_claims={'role': user.role},
                expires_delta=timedelta(hours=24)
            )
            
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )
            
            return {
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            return {'error': f'Login failed: {str(e)}'}, 500
    
    @staticmethod
    def get_user_profile(user_id):
        """
        Get user profile information
        Args:
            user_id: User ID from JWT token
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch profile: {str(e)}'}, 500
    
    @staticmethod
    def update_user_profile(user_id, data):
        """
        Update user profile
        Args:
            user_id: User ID from JWT token
            data: Dictionary containing fields to update
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            # Update email if provided
            if 'email' in data:
                # Check if new email is already taken
                existing = User.query.filter_by(email=data['email']).first()
                if existing and existing.id != user_id:
                    return {'error': 'Email already in use'}, 400
                user.email = data['email']
            
            # Update password if provided
            if 'password' in data:
                if len(data['password']) < 6:
                    return {'error': 'Password must be at least 6 characters'}, 400
                user.set_password(data['password'])
            
            db.session.commit()
            
            return {
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Update failed: {str(e)}'}, 500
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete user account
        Args:
            user_id: User ID to delete
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            db.session.delete(user)
            db.session.commit()
            
            return {
                'message': 'User deleted successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Deletion failed: {str(e)}'}, 500
    
    @staticmethod
    def get_all_users():
        """
        Get all users (admin only)
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            users = User.query.all()
            return {
                'users': [user.to_dict() for user in users],
                'count': len(users)
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch users: {str(e)}'}, 500