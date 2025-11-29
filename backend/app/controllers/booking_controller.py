from app.models.booking import Booking
from app.models.flight import Flight
from app.models.user import User
from app.extensions import db
from datetime import datetime
from marshmallow import ValidationError
from app.schemas.booking_schema import BookingCreateSchema, BookingUpdateSchema
from app.utils.pnr_generator import generate_pnr
from app.utils.dynamic_pricing import calculate_dynamic_price

class BookingController:
    """Controller for handling booking-related business logic"""
    
    @staticmethod
    def create_booking(user_id, data):
        """
        Create a new booking
        Args:
            user_id: ID of the user making the booking
            data: Dictionary containing booking details
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            # Validate input
            schema = BookingCreateSchema()
            validated_data = schema.load(data)
            
            flight_id = validated_data['flight_id']
            seat_number = validated_data['seat_number']
            passenger_name = validated_data['passenger_name']
            
            # Check if flight exists
            flight = Flight.query.filter_by(flight_id=flight_id).first()
            if not flight:
                return {'error': 'Flight not found'}, 404
            
            # Check if seat is available
            if seat_number not in flight.seats:
                return {'error': 'Invalid seat number'}, 400
            
            if flight.seats[seat_number]['status'] != 'available':
                return {'error': 'Seat is already booked'}, 400
            
            # Check if flight is in the past
            if flight.departure_time < datetime.utcnow():
                return {'error': 'Cannot book a flight in the past'}, 400
            
            # Generate PNR
            pnr = generate_pnr()
            
            # Check if PNR already exists (very unlikely but possible)
            while Booking.query.filter_by(pnr=pnr).first():
                pnr = generate_pnr()
            
            # Calculate final price with dynamic pricing
            final_price = calculate_dynamic_price(
                base_price=flight.price,
                available_seats=len(flight.get_available_seats()),
                total_seats=len(flight.seats),
                departure_time=flight.departure_time
            )
            
            # Create booking
            booking = Booking(
                pnr=pnr,
                user_id=user_id,
                flight_id=flight_id,
                passenger_name=passenger_name,
                seat_number=seat_number,
                status='confirmed',
                payment_status=validated_data.get('payment_status', 'completed')
            )
            
            # Mark seat as booked
            flight.seats[seat_number]['status'] = 'booked'
            flight.seats[seat_number]['passenger'] = passenger_name
            
            db.session.add(booking)
            db.session.commit()
            
            # Prepare response
            booking_dict = booking.to_dict()
            booking_dict['flight'] = {
                'airline': flight.airline,
                'source': flight.source,
                'destination': flight.destination,
                'departure_time': flight.departure_time.isoformat(),
                'arrival_time': flight.arrival_time.isoformat(),
                'price': final_price
            }
            
            return {
                'message': 'Booking created successfully',
                'booking': booking_dict
            }, 201
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Booking failed: {str(e)}'}, 500
    
    @staticmethod
    def get_user_bookings(user_id):
        """
        Get all bookings for a user
        Args:
            user_id: User ID
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            bookings = Booking.query.filter_by(user_id=user_id).order_by(
                Booking.booking_date.desc()
            ).all()
            
            booking_list = []
            for booking in bookings:
                booking_dict = booking.to_dict()
                
                # Add flight details
                flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
                if flight:
                    booking_dict['flight'] = {
                        'airline': flight.airline,
                        'source': flight.source,
                        'destination': flight.destination,
                        'departure_time': flight.departure_time.isoformat(),
                        'arrival_time': flight.arrival_time.isoformat()
                    }
                
                booking_list.append(booking_dict)
            
            return {
                'bookings': booking_list,
                'count': len(booking_list)
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch bookings: {str(e)}'}, 500
    
    @staticmethod
    def get_booking_by_pnr(pnr, user_id=None):
        """
        Get booking details by PNR
        Args:
            pnr: Booking PNR
            user_id: Optional user ID to verify ownership
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            booking = Booking.query.filter_by(pnr=pnr).first()
            
            if not booking:
                return {'error': 'Booking not found'}, 404
            
            # If user_id provided, verify ownership
            if user_id and booking.user_id != user_id:
                return {'error': 'Unauthorized access to booking'}, 403
            
            booking_dict = booking.to_dict()
            
            # Add flight details
            flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
            if flight:
                booking_dict['flight'] = {
                    'flight_id': flight.flight_id,
                    'airline': flight.airline,
                    'source': flight.source,
                    'destination': flight.destination,
                    'departure_time': flight.departure_time.isoformat(),
                    'arrival_time': flight.arrival_time.isoformat()
                }
            
            # Add user details
            user = User.query.get(booking.user_id)
            if user:
                booking_dict['user'] = {
                    'email': user.email
                }
            
            return {
                'booking': booking_dict
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch booking: {str(e)}'}, 500
    
    @staticmethod
    def cancel_booking(pnr, user_id):
        """
        Cancel a booking
        Args:
            pnr: Booking PNR
            user_id: User ID making the cancellation
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            booking = Booking.query.filter_by(pnr=pnr).first()
            
            if not booking:
                return {'error': 'Booking not found'}, 404
            
            # Verify ownership
            if booking.user_id != user_id:
                return {'error': 'Unauthorized to cancel this booking'}, 403
            
            # Check if already cancelled
            if booking.status == 'cancelled':
                return {'error': 'Booking is already cancelled'}, 400
            
            # Check if flight has already departed
            flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
            if flight and flight.departure_time < datetime.utcnow():
                return {'error': 'Cannot cancel a booking for a past flight'}, 400
            
            # Update booking status
            booking.status = 'cancelled'
            
            # Free up the seat
            if flight and booking.seat_number in flight.seats:
                flight.seats[booking.seat_number]['status'] = 'available'
                if 'passenger' in flight.seats[booking.seat_number]:
                    del flight.seats[booking.seat_number]['passenger']
            
            db.session.commit()
            
            return {
                'message': 'Booking cancelled successfully',
                'booking': booking.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Cancellation failed: {str(e)}'}, 500
    
    @staticmethod
    def update_booking(pnr, user_id, data):
        """
        Update booking details
        Args:
            pnr: Booking PNR
            user_id: User ID making the update
            data: Dictionary containing fields to update
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            booking = Booking.query.filter_by(pnr=pnr).first()
            
            if not booking:
                return {'error': 'Booking not found'}, 404
            
            # Verify ownership
            if booking.user_id != user_id:
                return {'error': 'Unauthorized to update this booking'}, 403
            
            # Check if booking is cancelled
            if booking.status == 'cancelled':
                return {'error': 'Cannot update a cancelled booking'}, 400
            
            # Validate input
            schema = BookingUpdateSchema()
            validated_data = schema.load(data)
            
            # Handle seat change
            if 'seat_number' in validated_data and validated_data['seat_number'] != booking.seat_number:
                new_seat = validated_data['seat_number']
                flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
                
                if not flight:
                    return {'error': 'Flight not found'}, 404
                
                # Check if new seat is available
                if new_seat not in flight.seats:
                    return {'error': 'Invalid seat number'}, 400
                
                if flight.seats[new_seat]['status'] != 'available':
                    return {'error': 'New seat is not available'}, 400
                
                # Free old seat and book new seat
                old_seat = booking.seat_number
                flight.seats[old_seat]['status'] = 'available'
                if 'passenger' in flight.seats[old_seat]:
                    del flight.seats[old_seat]['passenger']
                
                flight.seats[new_seat]['status'] = 'booked'
                flight.seats[new_seat]['passenger'] = booking.passenger_name
                
                booking.seat_number = new_seat
            
            # Update other fields
            if 'passenger_name' in validated_data:
                booking.passenger_name = validated_data['passenger_name']
            
            if 'status' in validated_data:
                booking.status = validated_data['status']
            
            if 'payment_status' in validated_data:
                booking.payment_status = validated_data['payment_status']
            
            db.session.commit()
            
            return {
                'message': 'Booking updated successfully',
                'booking': booking.to_dict()
            }, 200
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Update failed: {str(e)}'}, 500
    
    @staticmethod
    def get_all_bookings(page=1, per_page=20):
        """
        Get all bookings with pagination (admin only)
        Args:
            page: Page number
            per_page: Items per page
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            pagination = Booking.query.order_by(Booking.booking_date.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            bookings = []
            for booking in pagination.items:
                booking_dict = booking.to_dict()
                
                # Add flight details
                flight = Flight.query.filter_by(flight_id=booking.flight_id).first()
                if flight:
                    booking_dict['flight'] = {
                        'airline': flight.airline,
                        'source': flight.source,
                        'destination': flight.destination
                    }
                
                # Add user details
                user = User.query.get(booking.user_id)
                if user:
                    booking_dict['user'] = {
                        'email': user.email
                    }
                
                bookings.append(booking_dict)
            
            return {
                'bookings': bookings,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch bookings: {str(e)}'}, 500