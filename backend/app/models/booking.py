from app.extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    passenger_name = db.Column(db.String(200), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    payment_status = db.Column(db.String(20), default='completed')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        # Get the flight details using the database ID
        from app.models.flight import Flight
        flight = Flight.query.get(self.flight_id)
        
        result = {
            'pnr': self.pnr,
            'user_id': self.user_id,
            'flight_id': flight.flight_id if flight else None,
            'passenger_name': self.passenger_name,
            'seat_number': self.seat_number,
            'status': self.status,
            'payment_status': self.payment_status,
            'booking_date': self.booking_date.isoformat(),
        }
        
        # Add flight details if available
        if flight:
            result['flight'] = {
                'airline': flight.airline,
                'source': flight.source,
                'destination': flight.destination,
                'departure_time': flight.departure_time.isoformat(),
                'arrival_time': flight.arrival_time.isoformat(),
                'price': flight.price,
            }
            # Add seat class
            if self.seat_number in flight.seats:
                result['seat_class'] = flight.seats[self.seat_number].get('type', 'economy')
        
        return result