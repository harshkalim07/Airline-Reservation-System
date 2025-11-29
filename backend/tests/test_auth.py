import pytest
import json
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create a test user and return auth headers"""
    # Register a test user
    response = client.post('/api/auth/signup', 
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'testpass123'
        }),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    token = data.get('access_token')
    
    return {'Authorization': f'Bearer {token}'}

class TestAuthRoutes:
    """Test suite for authentication routes"""
    
    def test_signup_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'newuser@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_signup_duplicate_email(self, client):
        """Test registration with existing email"""
        # First registration
        client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'duplicate@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Duplicate registration
        response = client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'duplicate@example.com',
                'password': 'password456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_signup_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'invalidemail',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_signup_short_password(self, client):
        """Test registration with short password"""
        response = client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'user@example.com',
                'password': '12345'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user first
        client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'login@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Login
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'login@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_wrong_password(self, client):
        """Test login with incorrect password"""
        # Register user first
        client.post('/api/auth/signup',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'correctpass'
            }),
            content_type='application/json'
        )
        
        # Login with wrong password
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'wrongpass'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_get_profile(self, client, auth_headers):
        """Test getting user profile"""
        response = client.get('/api/auth/profile',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
    
    def test_get_profile_without_token(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/auth/profile')
        
        assert response.status_code == 401
    
    def test_update_profile(self, client, auth_headers):
        """Test updating user profile"""
        response = client.put('/api/auth/profile',
            headers=auth_headers,
            data=json.dumps({
                'email': 'updated@example.com'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['email'] == 'updated@example.com'
    
    def test_update_password(self, client, auth_headers):
        """Test updating password"""
        response = client.put('/api/auth/profile',
            headers=auth_headers,
            data=json.dumps({
                'password': 'newpassword123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200