from flask import Blueprint, request, jsonify
from app.models.booking import Booking
from app.models.flight import Flight
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, EXCLUDE
import random

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Bookings route is working!'}), 200

class BookingSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore extra fields
    
    flight_id = fields.Str(required=True)
    passenger_name = fields.Str(required=True)
    seat_number = fields.Str(required=True)

@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create new booking"""
    print("\n" + "="*50)
    print("🚀 CREATE BOOKING ENDPOINT HIT")
    print("="*50)
    
    try:
        user_id = get_jwt_identity()
        # Convert to int to match database
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
        print(f"👤 User ID: {user_id} (converted to {user_id_int})")
        
        # Log the raw request
        print(f"📥 Raw request.json: {request.json}")
        print(f"📥 Request data type: {type(request.json)}")
        
        # Manual validation first
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['flight_id', 'passenger_name', 'seat_number']
        for field in required_fields:
            if field not in request.json:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            if not isinstance(request.json[field], str):
                return jsonify({'error': f'{field} must be a string, got {type(request.json[field])}'}), 400
        
        # Now try schema validation
        schema = BookingSchema()
        print("🔍 About to validate with schema...")
        
        try:
            data = schema.load(request.json)
            print(f"✅ Schema validation passed: {data}")
        except ValidationError as ve:
            print(f"❌ Schema validation failed: {ve.messages}")
            return jsonify({'error': ve.messages}), 422
        
        # Check if flight exists
        flight = Flight.query.filter_by(flight_id=data['flight_id']).first()
        if not flight:
            print(f"❌ Flight {data['flight_id']} not found")
            return jsonify({'error': 'Flight not found'}), 404
        
        print(f"✅ Flight found: {flight.flight_id}")
        
        # Check seat availability
        seat = data['seat_number']
        print(f"🪑 Checking seat: {seat}")
        
        if seat not in flight.seats:
            print(f"❌ Seat {seat} does not exist in flight.seats")
            print(f"Available seats: {list(flight.seats.keys())[:10]}")
            return jsonify({'error': f'Seat {seat} does not exist'}), 400
        
        print(f"✅ Seat exists: {flight.seats[seat]}")
            
        if flight.seats[seat]['status'] != 'available':
            print(f"❌ Seat {seat} status is: {flight.seats[seat]['status']}")
            return jsonify({'error': f'Seat {seat} is not available'}), 400
        
        print("✅ Seat is available")
        
        # Generate PNR
        pnr = f"PNR{random.randint(100000, 999999)}"
        print(f"🎫 Generated PNR: {pnr}")
        
        # Create booking with integer user_id
        booking = Booking(
            pnr=pnr,
            user_id=user_id_int,
            flight_id=data['flight_id'],
            passenger_name=data['passenger_name'],
            seat_number=seat,
            status='confirmed',
            payment_status='completed'
        )
        
        print("✅ Booking object created")
        
        # Update seat status
        flight.seats[seat]['status'] = 'booked'
        flight.seats = flight.seats.copy()  # Trigger update
        
        print("✅ Seat marked as booked")
        
        db.session.add(booking)
        db.session.commit()
        
        print(f"✅ Database committed successfully")
        print(f"🎉 BOOKING SUCCESSFUL: {pnr}")
        print("="*50 + "\n")
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        print(f"❌ UNEXPECTED EXCEPTION: {type(e).__name__}")
        print(f"❌ Exception message: {str(e)}")
        import traceback
        print(f"❌ Traceback:\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get user's booking history"""
    try:
        user_id = get_jwt_identity()
        # Convert to int to match database
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
        
        bookings = Booking.query.filter_by(user_id=user_id_int).order_by(
            Booking.booking_date.desc()
        ).all()
        
        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/<string:pnr>', methods=['GET'])
@jwt_required()
def get_booking(pnr):
    """Get booking by PNR"""
    try:
        user_id = get_jwt_identity()
        # Convert to int to match database
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
        
        booking = Booking.query.filter_by(pnr=pnr, user_id=user_id_int).first()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        return jsonify(booking.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/<string:pnr>/cancel', methods=['PUT'])
@jwt_required()
def cancel_booking(pnr):
    """Cancel booking"""
    try:
        user_id = get_jwt_identity()
        # Convert to int to match database
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
        
        booking = Booking.query.filter_by(pnr=pnr, user_id=user_id_int).first()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        if booking.status == 'cancelled':
            return jsonify({'error': 'Booking already cancelled'}), 400
        
        # Update booking status
        booking.status = 'cancelled'
        
        # Free up the seat
        flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
        if flight:
            flight.seats[booking.seat_number]['status'] = 'available'
            flight.seats = flight.seats.copy()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500