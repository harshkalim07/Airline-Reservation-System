from app import create_app, db
from app.models.flight import Flight

app = create_app()

def reset_all_seats():
    """Reset all seats in all flights to available status"""
    with app.app_context():
        print("🔄 Resetting all seats to available...")
        
        # Generate fresh seats layout
        def generate_seats():
            seats = {}
            # Business class (rows 1-5): A, B, C, D
            for row in range(1, 6):
                for letter in ['A', 'B', 'C', 'D']:
                    seat = f"{row}{letter}"
                    seats[seat] = {'status': 'available', 'type': 'business'}
            
            # Premium Economy (rows 6-10): A, B, C, D, E, F
            for row in range(6, 11):
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    seat = f"{row}{letter}"
                    seats[seat] = {'status': 'available', 'type': 'premium_economy'}
            
            # Economy class (rows 11-30): A, B, C, D, E, F
            for row in range(11, 31):
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    seat = f"{row}{letter}"
                    seats[seat] = {'status': 'available', 'type': 'economy'}
            
            return seats
        
        # Get all flights
        flights = Flight.query.all()
        total_flights = len(flights)
        
        print(f"📊 Found {total_flights} flights")
        print(f"🎫 Resetting seats for each flight (170 seats per flight)...")
        
        # Reset seats for each flight
        fresh_seats = generate_seats()
        for i, flight in enumerate(flights, 1):
            flight.seats = fresh_seats.copy()
            
            if i % 100 == 0:
                print(f"   ✓ Processed {i}/{total_flights} flights")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Successfully reset {total_flights} flights!")
        print(f"💺 Each flight now has 170 available seats")
        print(f"   - Business: 20 seats (rows 1-5)")
        print(f"   - Premium Economy: 30 seats (rows 6-10)")
        print(f"   - Economy: 120 seats (rows 11-30)")
        print(f"\n🎉 All flights are now bookable!")

if __name__ == '__main__':
    reset_all_seats()