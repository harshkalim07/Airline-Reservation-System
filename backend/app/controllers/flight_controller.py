from app.models.flight import Flight
from app.extensions import db
from datetime import datetime, timedelta
from marshmallow import ValidationError
from app.schemas.flight_schema import FlightCreateSchema, FlightUpdateSchema, FlightSearchSchema
from app.utils.dynamic_pricing import calculate_dynamic_price
import random

class FlightController:
    """Controller for handling flight-related business logic"""
    
    @staticmethod
    def create_flight(data):
        """
        Create a new flight
        Args:
            data: Dictionary containing flight details
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            # Validate input
            schema = FlightCreateSchema()
            validated_data = schema.load(data)
            
            # Check if flight_id already exists
            existing_flight = Flight.query.filter_by(flight_id=validated_data['flight_id']).first()
            if existing_flight:
                return {'error': 'Flight ID already exists'}, 400
            
            # Validate times
            if validated_data['departure_time'] >= validated_data['arrival_time']:
                return {'error': 'Arrival time must be after departure time'}, 400
            
            # Create flight
            flight = Flight(
                flight_id=validated_data['flight_id'],
                airline=validated_data['airline'],
                source=validated_data['source'],
                destination=validated_data['destination'],
                departure_time=validated_data['departure_time'],
                arrival_time=validated_data['arrival_time'],
                price=validated_data['price'],
                seats=validated_data.get('seats', FlightController._generate_default_seats())
            )
            
            db.session.add(flight)
            db.session.commit()
            
            return {
                'message': 'Flight created successfully',
                'flight': flight.to_dict()
            }, 201
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create flight: {str(e)}'}, 500
    
    @staticmethod
    def _generate_default_seats():
        """Generate default seat layout"""
        seats = {}
        rows = 30
        seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for row in range(1, rows + 1):
            for letter in seat_letters:
                seat_number = f"{row}{letter}"
                seats[seat_number] = {
                    'status': 'available',
                    'type': 'economy' if row > 5 else 'business'
                }
        
        return seats
    
    @staticmethod
    def search_flights(query_params):
        """
        Search for flights based on criteria
        Args:
            query_params: Dictionary containing search parameters
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            # Validate search parameters
            schema = FlightSearchSchema()
            validated_params = schema.load(query_params)
            
            source = validated_params['source']
            destination = validated_params['destination']
            date = validated_params['date']
            passengers = validated_params.get('passengers', 1)
            
            # Query flights
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            
            flights = Flight.query.filter(
                Flight.source.ilike(f'%{source}%'),
                Flight.destination.ilike(f'%{destination}%'),
                Flight.departure_time.between(start_of_day, end_of_day)
            ).all()
            
            # Filter by available seats and calculate dynamic pricing
            available_flights = []
            for flight in flights:
                available_seats = flight.get_available_seats()
                
                if len(available_seats) >= passengers:
                    flight_dict = flight.to_dict()
                    flight_dict['available_seats'] = len(available_seats)
                    
                    # Apply dynamic pricing
                    dynamic_price = calculate_dynamic_price(
                        base_price=flight.price,
                        available_seats=len(available_seats),
                        total_seats=len(flight.seats),
                        departure_time=flight.departure_time
                    )
                    flight_dict['price'] = dynamic_price
                    
                    available_flights.append(flight_dict)
            
            return {
                'flights': available_flights,
                'count': len(available_flights)
            }, 200
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            return {'error': f'Search failed: {str(e)}'}, 500
    
    @staticmethod
    def get_flight_by_id(flight_id):
        """
        Get flight details by ID
        Args:
            flight_id: Flight identifier
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            flight = Flight.query.filter_by(flight_id=flight_id).first()
            
            if not flight:
                return {'error': 'Flight not found'}, 404
            
            flight_dict = flight.to_dict()
            flight_dict['available_seats'] = len(flight.get_available_seats())
            
            return {
                'flight': flight_dict
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch flight: {str(e)}'}, 500
    
    @staticmethod
    def update_flight(flight_id, data):
        """
        Update flight information
        Args:
            flight_id: Flight identifier
            data: Dictionary containing fields to update
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            flight = Flight.query.filter_by(flight_id=flight_id).first()
            
            if not flight:
                return {'error': 'Flight not found'}, 404
            
            # Validate input
            schema = FlightUpdateSchema()
            validated_data = schema.load(data)
            
            # Update fields
            for key, value in validated_data.items():
                if hasattr(flight, key):
                    setattr(flight, key, value)
            
            # Validate times if both are provided
            if flight.departure_time >= flight.arrival_time:
                return {'error': 'Arrival time must be after departure time'}, 400
            
            db.session.commit()
            
            return {
                'message': 'Flight updated successfully',
                'flight': flight.to_dict()
            }, 200
            
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Update failed: {str(e)}'}, 500
    
    @staticmethod
    def delete_flight(flight_id):
        """
        Delete a flight
        Args:
            flight_id: Flight identifier
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            flight = Flight.query.filter_by(flight_id=flight_id).first()
            
            if not flight:
                return {'error': 'Flight not found'}, 404
            
            # Check if there are active bookings
            from app.models.booking import Booking
            active_bookings = Booking.query.filter_by(
                flight_id=flight_id,
                status='confirmed'
            ).count()
            
            if active_bookings > 0:
                return {
                    'error': f'Cannot delete flight with {active_bookings} active bookings'
                }, 400
            
            db.session.delete(flight)
            db.session.commit()
            
            return {
                'message': 'Flight deleted successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Deletion failed: {str(e)}'}, 500
    
    @staticmethod
    def get_all_flights(page=1, per_page=20):
        """
        Get all flights with pagination
        Args:
            page: Page number
            per_page: Items per page
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            pagination = Flight.query.order_by(Flight.departure_time).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            flights = []
            for flight in pagination.items:
                flight_dict = flight.to_dict()
                flight_dict['available_seats'] = len(flight.get_available_seats())
                flights.append(flight_dict)
            
            return {
                'flights': flights,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch flights: {str(e)}'}, 500
    
    @staticmethod
    def get_available_seats(flight_id):
        """
        Get available seats for a flight
        Args:
            flight_id: Flight identifier
        Returns:
            Tuple of (result_dict, status_code)
        """
        try:
            flight = Flight.query.filter_by(flight_id=flight_id).first()
            
            if not flight:
                return {'error': 'Flight not found'}, 404
            
            available_seats = flight.get_available_seats()
            
            return {
                'flight_id': flight_id,
                'available_seats': available_seats,
                'count': len(available_seats)
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to fetch seats: {str(e)}'}, 500