from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

def token_required(f):
    """
    Decorator to protect routes that require authentication
    Usage: @token_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Authentication required',
                'message': str(e)
            }), 401
    
    return decorated_function

def get_current_user():
    """
    Get the current authenticated user's ID from JWT token
    Returns:
        User ID or None
    """
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        return None

def get_current_user_role():
    """
    Get the current authenticated user's role from JWT token
    Returns:
        User role or None
    """
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        return claims.get('role', 'user')
    except Exception:
        return None

def optional_token(f):
    """
    Decorator for routes where authentication is optional
    Usage: @optional_token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass
        return f(*args, **kwargs)
    
    return decorated_function