from app.extensions import db
from datetime import datetime
import json

class Flight(db.Model):
    __tablename__ = 'flights'
    
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    airline = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False, index=True)
    destination = db.Column(db.String(100), nullable=False, index=True)
    departure_time = db.Column(db.DateTime, nullable=False, index=True)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seats = db.Column(db.JSON, default={})  # {"A1": {"status": "available"}, ...}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    bookings = db.relationship('Booking', backref='flight', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,  # Database ID
            'flight_id': self.flight_id,  # Flight code like "AI101"
            'airline': self.airline,
            'source': self.source,
            'destination': self.destination,
            'departure_time': self.departure_time.isoformat(),
            'arrival_time': self.arrival_time.isoformat(),
            'price': self.price,
            'seats': self.seats
        }
    
    def get_available_seats(self):
        return [seat for seat, data in self.seats.items() if data.get('status') == 'available']
    
    def book_seat(self, seat_number):
        if seat_number in self.seats and self.seats[seat_number]['status'] == 'available':
            self.seats[seat_number]['status'] = 'booked'
            db.session.commit()
            return True
        return False