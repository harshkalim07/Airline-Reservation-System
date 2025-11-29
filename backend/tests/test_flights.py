import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.flight import Flight
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
def admin_headers(client):
    """Create admin user and return auth headers"""
    response = client.post('/api/auth/signup',
        data=json.dumps({
            'email': 'admin@example.com',
            'password': 'adminpass123',
            'role': 'admin'
        }),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    token = data.get('access_token')
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_flight(app):
    """Create a sample flight for testing"""
    with app.app_context():
        departure = datetime.utcnow() + timedelta(days=7)
        arrival = departure + timedelta(hours=2)
        
        flight = Flight(
            flight_id='TEST123',
            airline='Test Airlines',
            source='Mumbai',
            destination='Delhi',
            departure_time=departure,
            arrival_time=arrival,
            price=5000.0,
            seats={
                '1A': {'status': 'available', 'type': 'business'},
                '1B': {'status': 'available', 'type': 'business'},
                '2A': {'status': 'available', 'type': 'economy'},
                '2B': {'status': 'available', 'type': 'economy'},
            }
        )
        
        db.session.add(flight)
        db.session.commit()
        
        return flight.flight_id

class TestFlightRoutes:
    """Test suite for flight routes"""
    
    def test_create_flight(self, client, admin_headers):
        """Test creating a new flight"""
        departure = (datetime.utcnow() + timedelta(days=10)).isoformat()
        arrival = (datetime.utcnow() + timedelta(days=10, hours=3)).isoformat()
        
        response = client.post('/api/flights',
            headers=admin_headers,
            data=json.dumps({
                'flight_id': 'AI101',
                'airline': 'Air India',
                'source': 'Mumbai',
                'destination': 'Bangalore',
                'departure_time': departure,
                'arrival_time': arrival,
                'price': 4500.0
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['flight']['flight_id'] == 'AI101'
    
    def test_create_flight_duplicate_id(self, client, admin_headers, sample_flight):
        """Test creating flight with duplicate ID"""
        departure = (datetime.utcnow() + timedelta(days=10)).isoformat()
        arrival = (datetime.utcnow() + timedelta(days=10, hours=3)).isoformat()
        
        response = client.post('/api/flights',
            headers=admin_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'airline': 'Test Airlines',
                'source': 'Mumbai',
                'destination': 'Delhi',
                'departure_time': departure,
                'arrival_time': arrival,
                'price': 5000.0
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_search_flights(self, client, sample_flight):
        """Test searching for flights"""
        search_date = (datetime.utcnow() + timedelta(days=7)).date().isoformat()
        
        response = client.get(
            f'/api/flights/search?source=Mumbai&destination=Delhi&date={search_date}',
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'flights' in data
        assert len(data['flights']) > 0
    
    def test_search_flights_no_results(self, client):
        """Test searching flights with no results"""
        search_date = (datetime.utcnow() + timedelta(days=7)).date().isoformat()
        
        response = client.get(
            f'/api/flights/search?source=NonExistent&destination=City&date={search_date}',
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_get_flight_by_id(self, client, sample_flight):
        """Test getting flight details by ID"""
        response = client.get(f'/api/flights/{sample_flight}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['flight']['id'] == sample_flight
    
    def test_get_nonexistent_flight(self, client):
        """Test getting non-existent flight"""
        response = client.get('/api/flights/NONEXISTENT')
        
        assert response.status_code == 404
    
    def test_update_flight(self, client, admin_headers, sample_flight):
        """Test updating flight details"""
        response = client.put(f'/api/flights/{sample_flight}',
            headers=admin_headers,
            data=json.dumps({
                'price': 6000.0
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['flight']['price'] == 6000.0
    
    def test_delete_flight(self, client, admin_headers, sample_flight):
        """Test deleting a flight"""
        response = client.delete(f'/api/flights/{sample_flight}',
            headers=admin_headers
        )
        
        assert response.status_code == 200
    
    def test_get_available_seats(self, client, sample_flight):
        """Test getting available seats for a flight"""
        response = client.get(f'/api/flights/{sample_flight}/seats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'available_seats' in data
        assert data['count'] > 0
    
    def test_get_all_flights(self, client, sample_flight):
        """Test getting all flights"""
        response = client.get('/api/flights')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'flights' in data