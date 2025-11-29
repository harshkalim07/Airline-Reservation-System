from flask import Blueprint, request, jsonify
from app.models.flight import Flight
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from marshmallow import Schema, fields, ValidationError

flights_bp = Blueprint('flights', __name__)

class FlightSchema(Schema):
    airline = fields.Str(required=True)
    source = fields.Str(required=True)
    destination = fields.Str(required=True)
    departure_time = fields.DateTime(required=True)
    arrival_time = fields.DateTime(required=True)
    price = fields.Float(required=True)

def admin_required():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None

@flights_bp.route('/search', methods=['GET'])
def search_flights():
    """Search for flights"""
    try:
        source = request.args.get('source', '').strip()
        destination = request.args.get('destination', '').strip()
        date = request.args.get('date', '').strip()
        
        if not source or not destination or not date:
            return jsonify({
                'error': 'Source, destination, and date are required'
            }), 400
        
        # Parse date
        try:
            date_obj = datetime.fromisoformat(date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Query flights (case insensitive)
        query = Flight.query.filter(
            db.func.lower(Flight.source) == source.lower(),
            db.func.lower(Flight.destination) == destination.lower(),
            db.func.date(Flight.departure_time) == date_obj.date()
        )
        
        flights = query.all()
        
        # Add available seats count to each flight
        flights_data = []
        for flight in flights:
            flight_dict = flight.to_dict()
            flight_dict['available_seats'] = len(flight.get_available_seats())
            flights_data.append(flight_dict)
        
        return jsonify({
            'flights': flights_data,
            'count': len(flights_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flights_bp.route('', methods=['GET'])
def get_flights():
    """Get all flights with optional filters"""
    try:
        # Get query parameters
        source = request.args.get('source', '').lower()
        destination = request.args.get('destination', '').lower()
        date = request.args.get('date')
        
        # Base query
        query = Flight.query
        
        # Apply filters
        if source:
            query = query.filter(db.func.lower(Flight.source) == source)
        if destination:
            query = query.filter(db.func.lower(Flight.destination) == destination)
        if date:
            date_obj = datetime.fromisoformat(date)
            query = query.filter(db.func.date(Flight.departure_time) == date_obj.date())
        
        flights = query.all()
        
        return jsonify({
            'flights': [flight.to_dict() for flight in flights]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flights_bp.route('/<string:flight_id>', methods=['GET'])
def get_flight(flight_id):
    """Get single flight by ID"""
    try:
        flight = Flight.query.filter_by(flight_id=flight_id).first()
        
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404
        
        flight_dict = flight.to_dict()
        flight_dict['available_seats'] = len(flight.get_available_seats())
        
        return jsonify({'flight': flight_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flights_bp.route('/<string:flight_id>/seats', methods=['GET'])
def get_available_seats(flight_id):
    """Get available seats for a flight"""
    try:
        flight = Flight.query.filter_by(flight_id=flight_id).first()
        
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404
        
        available_seats = flight.get_available_seats()
        
        return jsonify({
            'flight_id': flight_id,
            'available_seats': available_seats,
            'count': len(available_seats)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flights_bp.route('', methods=['POST'])
@jwt_required()
def create_flight():
    """Create new flight (Admin only)"""
    # Check admin
    error_response = admin_required()
    if error_response:
        return error_response
    
    try:
        schema = FlightSchema()
        data = schema.load(request.json)
        
        # Generate flight ID
        import random
        flight_id = f"FL{random.randint(100000, 999999)}"
        
        # Initialize seats (A1-A6, B1-B6, C1-C6)
        seats = {}
        for row in ['A', 'B', 'C']:
            for num in range(1, 7):
                seats[f"{row}{num}"] = {"status": "available"}
        
        # Create flight
        flight = Flight(
            flight_id=flight_id,
            airline=data['airline'],
            source=data['source'],
            destination=data['destination'],
            departure_time=data['departure_time'],
            arrival_time=data['arrival_time'],
            price=data['price'],
            seats=seats
        )
        
        db.session.add(flight)
        db.session.commit()
        
        return jsonify({
            'message': 'Flight created successfully',
            'flight': flight.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@flights_bp.route('/<string:flight_id>', methods=['PUT'])
@jwt_required()
def update_flight(flight_id):
    """Update flight (Admin only)"""
    error_response = admin_required()
    if error_response:
        return error_response
    
    try:
        flight = Flight.query.filter_by(flight_id=flight_id).first()
        
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404
        
        data = request.json
        
        if 'airline' in data:
            flight.airline = data['airline']
        if 'source' in data:
            flight.source = data['source']
        if 'destination' in data:
            flight.destination = data['destination']
        if 'departure_time' in data:
            flight.departure_time = datetime.fromisoformat(data['departure_time'])
        if 'arrival_time' in data:
            flight.arrival_time = datetime.fromisoformat(data['arrival_time'])
        if 'price' in data:
            flight.price = float(data['price'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Flight updated successfully',
            'flight': flight.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@flights_bp.route('/<string:flight_id>', methods=['DELETE'])
@jwt_required()
def delete_flight(flight_id):
    """Delete flight (Admin only)"""
    error_response = admin_required()
    if error_response:
        return error_response
    
    try:
        flight = Flight.query.filter_by(flight_id=flight_id).first()
        
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404
        
        db.session.delete(flight)
        db.session.commit()
        
        return jsonify({'message': 'Flight deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500