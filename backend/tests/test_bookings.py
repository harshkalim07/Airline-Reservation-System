import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.flight import Flight
from app.models.booking import Booking
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
    response = client.post('/api/auth/signup',
        data=json.dumps({
            'email': 'user@example.com',
            'password': 'userpass123'
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
            flight_id='BK123',
            airline='Booking Test Airlines',
            source='Mumbai',
            destination='Bangalore',
            departure_time=departure,
            arrival_time=arrival,
            price=4000.0,
            seats={
                '1A': {'status': 'available', 'type': 'economy'},
                '1B': {'status': 'available', 'type': 'economy'},
                '2A': {'status': 'available', 'type': 'economy'},
                '2B': {'status': 'booked', 'type': 'economy'},
            }
        )
        
        db.session.add(flight)
        db.session.commit()
        
        return flight.flight_id

class TestBookingRoutes:
    """Test suite for booking routes"""
    
    def test_create_booking(self, client, auth_headers, sample_flight):
        """Test creating a new booking"""
        response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'pnr' in data['booking']
        assert data['booking']['passenger'] == 'John Doe'
    
    def test_create_booking_invalid_seat(self, client, auth_headers, sample_flight):
        """Test booking with invalid seat"""
        response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '99Z'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_booking_already_booked_seat(self, client, auth_headers, sample_flight):
        """Test booking an already booked seat"""
        response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'Jane Doe',
                'seat_number': '2B'  # Already booked
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_booking_nonexistent_flight(self, client, auth_headers):
        """Test booking with non-existent flight"""
        response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': 'NONEXISTENT',
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_get_user_bookings(self, client, auth_headers, sample_flight):
        """Test getting user's bookings"""
        # Create a booking first
        client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        # Get bookings
        response = client.get('/api/bookings/my-bookings',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'bookings' in data
        assert len(data['bookings']) > 0
    
    def test_get_booking_by_pnr(self, client, auth_headers, sample_flight):
        """Test getting booking by PNR"""
        # Create a booking first
        booking_response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        booking_data = json.loads(booking_response.data)
        pnr = booking_data['booking']['pnr']
        
        # Get booking by PNR
        response = client.get(f'/api/bookings/{pnr}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['booking']['pnr'] == pnr
    
    def test_get_nonexistent_booking(self, client, auth_headers):
        """Test getting non-existent booking"""
        response = client.get('/api/bookings/NONEXISTENT',
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_cancel_booking(self, client, auth_headers, sample_flight):
        """Test cancelling a booking"""
        # Create a booking first
        booking_response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        booking_data = json.loads(booking_response.data)
        pnr = booking_data['booking']['pnr']
        
        # Cancel booking
        response = client.delete(f'/api/bookings/{pnr}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['booking']['status'] == 'cancelled'
    
    def test_cancel_already_cancelled_booking(self, client, auth_headers, sample_flight):
        """Test cancelling an already cancelled booking"""
        # Create and cancel a booking
        booking_response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        booking_data = json.loads(booking_response.data)
        pnr = booking_data['booking']['pnr']
        
        # First cancellation
        client.delete(f'/api/bookings/{pnr}', headers=auth_headers)
        
        # Second cancellation attempt
        response = client.delete(f'/api/bookings/{pnr}', headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_update_booking(self, client, auth_headers, sample_flight):
        """Test updating booking details"""
        # Create a booking
        booking_response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        booking_data = json.loads(booking_response.data)
        pnr = booking_data['booking']['pnr']
        
        # Update passenger name
        response = client.put(f'/api/bookings/{pnr}',
            headers=auth_headers,
            data=json.dumps({
                'passenger_name': 'John Smith'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['booking']['passenger'] == 'John Smith'
    
    def test_change_seat(self, client, auth_headers, sample_flight):
        """Test changing seat in a booking"""
        # Create a booking
        booking_response = client.post('/api/bookings',
            headers=auth_headers,
            data=json.dumps({
                'flight_id': sample_flight,
                'passenger_name': 'John Doe',
                'seat_number': '1A'
            }),
            content_type='application/json'
        )
        
        booking_data = json.loads(booking_response.data)
        pnr = booking_data['booking']['pnr']
        
        # Change seat
        response = client.put(f'/api/bookings/{pnr}',
            headers=auth_headers,
            data=json.dumps({
                'seat_number': '2A'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['booking']['seat'] == '2A'