from app import create_app, db
from app.models.flight import Flight
from datetime import datetime, timedelta
import random

app = create_app()

def seed_flights():
    with app.app_context():
        # Clear existing flights
        print("🗑️  Clearing existing flights...")
        Flight.query.delete()
        
        # Generate seats layout
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
        
        # Airlines with their characteristics
        airlines_info = {
            'Air India': {'prefix': 'AI', 'price_multiplier': 1.2, 'quality': 'premium'},
            'Vistara': {'prefix': 'UK', 'price_multiplier': 1.25, 'quality': 'premium'},
            'IndiGo': {'prefix': '6E', 'price_multiplier': 1.0, 'quality': 'standard'},
            'SpiceJet': {'prefix': 'SG', 'price_multiplier': 0.95, 'quality': 'standard'},
            'GoAir': {'prefix': 'G8', 'price_multiplier': 0.9, 'quality': 'budget'},
            'AirAsia India': {'prefix': 'I5', 'price_multiplier': 0.85, 'quality': 'budget'}
        }
        
        # Major Indian cities
        cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
            'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
            'Kochi', 'Goa', 'Chandigarh', 'Srinagar', 'Amritsar',
            'Bhubaneswar', 'Indore', 'Coimbatore', 'Vadodara', 'Nagpur'
        ]
        
        # Define routes with base prices and flight durations
        routes_info = {
            # Tier 1: Major metro routes (highest frequency)
            ('Mumbai', 'Delhi'): {'base_price': 4500, 'duration': 2.5, 'frequency': 'high'},
            ('Delhi', 'Mumbai'): {'base_price': 4500, 'duration': 2.5, 'frequency': 'high'},
            ('Mumbai', 'Bangalore'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'high'},
            ('Bangalore', 'Mumbai'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'high'},
            ('Delhi', 'Bangalore'): {'base_price': 5500, 'duration': 3.0, 'frequency': 'high'},
            ('Bangalore', 'Delhi'): {'base_price': 5500, 'duration': 3.0, 'frequency': 'high'},
            ('Mumbai', 'Hyderabad'): {'base_price': 3200, 'duration': 1.5, 'frequency': 'high'},
            ('Hyderabad', 'Mumbai'): {'base_price': 3200, 'duration': 1.5, 'frequency': 'high'},
            ('Delhi', 'Chennai'): {'base_price': 5000, 'duration': 2.5, 'frequency': 'high'},
            ('Chennai', 'Delhi'): {'base_price': 5000, 'duration': 2.5, 'frequency': 'high'},
            ('Mumbai', 'Chennai'): {'base_price': 4800, 'duration': 2.0, 'frequency': 'high'},
            ('Chennai', 'Mumbai'): {'base_price': 4800, 'duration': 2.0, 'frequency': 'high'},
            ('Mumbai', 'Kolkata'): {'base_price': 5200, 'duration': 2.5, 'frequency': 'medium'},
            ('Kolkata', 'Mumbai'): {'base_price': 5200, 'duration': 2.5, 'frequency': 'medium'},
            ('Delhi', 'Kolkata'): {'base_price': 4800, 'duration': 2.0, 'frequency': 'medium'},
            ('Kolkata', 'Delhi'): {'base_price': 4800, 'duration': 2.0, 'frequency': 'medium'},
            
            # Tier 2: Important routes
            ('Bangalore', 'Hyderabad'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            ('Hyderabad', 'Bangalore'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            ('Bangalore', 'Chennai'): {'base_price': 2800, 'duration': 1.0, 'frequency': 'medium'},
            ('Chennai', 'Bangalore'): {'base_price': 2800, 'duration': 1.0, 'frequency': 'medium'},
            ('Delhi', 'Hyderabad'): {'base_price': 4500, 'duration': 2.0, 'frequency': 'medium'},
            ('Hyderabad', 'Delhi'): {'base_price': 4500, 'duration': 2.0, 'frequency': 'medium'},
            ('Mumbai', 'Pune'): {'base_price': 1200, 'duration': 0.5, 'frequency': 'high'},
            ('Pune', 'Mumbai'): {'base_price': 1200, 'duration': 0.5, 'frequency': 'high'},
            ('Mumbai', 'Ahmedabad'): {'base_price': 2000, 'duration': 1.0, 'frequency': 'medium'},
            ('Ahmedabad', 'Mumbai'): {'base_price': 2000, 'duration': 1.0, 'frequency': 'medium'},
            ('Delhi', 'Jaipur'): {'base_price': 1500, 'duration': 1.0, 'frequency': 'medium'},
            ('Jaipur', 'Delhi'): {'base_price': 1500, 'duration': 1.0, 'frequency': 'medium'},
            ('Delhi', 'Chandigarh'): {'base_price': 1800, 'duration': 1.0, 'frequency': 'medium'},
            ('Chandigarh', 'Delhi'): {'base_price': 1800, 'duration': 1.0, 'frequency': 'medium'},
            
            # Tier 3: Tourist & leisure routes
            ('Mumbai', 'Goa'): {'base_price': 2000, 'duration': 1.0, 'frequency': 'high'},
            ('Goa', 'Mumbai'): {'base_price': 2000, 'duration': 1.0, 'frequency': 'high'},
            ('Delhi', 'Goa'): {'base_price': 4000, 'duration': 2.5, 'frequency': 'medium'},
            ('Goa', 'Delhi'): {'base_price': 4000, 'duration': 2.5, 'frequency': 'medium'},
            ('Bangalore', 'Goa'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            ('Goa', 'Bangalore'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            ('Bangalore', 'Kochi'): {'base_price': 2800, 'duration': 1.0, 'frequency': 'medium'},
            ('Kochi', 'Bangalore'): {'base_price': 2800, 'duration': 1.0, 'frequency': 'medium'},
            ('Mumbai', 'Kochi'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'medium'},
            ('Kochi', 'Mumbai'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'medium'},
            ('Delhi', 'Srinagar'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'low'},
            ('Srinagar', 'Delhi'): {'base_price': 3500, 'duration': 1.5, 'frequency': 'low'},
            ('Delhi', 'Amritsar'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            ('Amritsar', 'Delhi'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'medium'},
            
            # Tier 4: Regional routes
            ('Delhi', 'Lucknow'): {'base_price': 2200, 'duration': 1.0, 'frequency': 'medium'},
            ('Lucknow', 'Delhi'): {'base_price': 2200, 'duration': 1.0, 'frequency': 'medium'},
            ('Kolkata', 'Bhubaneswar'): {'base_price': 1800, 'duration': 1.0, 'frequency': 'low'},
            ('Bhubaneswar', 'Kolkata'): {'base_price': 1800, 'duration': 1.0, 'frequency': 'low'},
            ('Mumbai', 'Indore'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'low'},
            ('Indore', 'Mumbai'): {'base_price': 2500, 'duration': 1.0, 'frequency': 'low'},
            ('Bangalore', 'Coimbatore'): {'base_price': 1800, 'duration': 0.75, 'frequency': 'low'},
            ('Coimbatore', 'Bangalore'): {'base_price': 1800, 'duration': 0.75, 'frequency': 'low'},
            ('Mumbai', 'Nagpur'): {'base_price': 2200, 'duration': 1.0, 'frequency': 'low'},
            ('Nagpur', 'Mumbai'): {'base_price': 2200, 'duration': 1.0, 'frequency': 'low'},
            ('Ahmedabad', 'Vadodara'): {'base_price': 900, 'duration': 0.5, 'frequency': 'low'},
            ('Vadodara', 'Ahmedabad'): {'base_price': 900, 'duration': 0.5, 'frequency': 'low'},
        }
        
        # Departure time slots
        departure_slots = [
            {'hour': 6, 'minute': 0, 'type': 'early_morning', 'discount': 0.85},
            {'hour': 7, 'minute': 30, 'type': 'morning', 'discount': 0.90},
            {'hour': 9, 'minute': 0, 'type': 'morning', 'discount': 1.0},
            {'hour': 10, 'minute': 30, 'type': 'mid_morning', 'discount': 1.05},
            {'hour': 12, 'minute': 0, 'type': 'noon', 'discount': 1.0},
            {'hour': 14, 'minute': 0, 'type': 'afternoon', 'discount': 1.0},
            {'hour': 16, 'minute': 30, 'type': 'evening', 'discount': 1.10},
            {'hour': 18, 'minute': 0, 'type': 'evening', 'discount': 1.15},
            {'hour': 20, 'minute': 0, 'type': 'night', 'discount': 0.95},
            {'hour': 22, 'minute': 0, 'type': 'late_night', 'discount': 0.80},
        ]
        
        flights_data = []
        flight_counter = 1000
        
        # Calculate December date range
        current_date = datetime.now()
        december_start = datetime(2025, 12, 1)
        december_end = datetime(2025, 12, 31)
        
        # Generate flights for entire December
        print(f"📅 Generating flights for December 2025 (31 days)...")
        
        for route, info in routes_info.items():
            source, destination = route
            base_price = info['base_price']
            duration = info['duration']
            frequency = info['frequency']
            
            # Determine flights per day based on frequency
            if frequency == 'high':
                flights_per_day = random.randint(6, 8)  # 6-8 flights per day
            elif frequency == 'medium':
                flights_per_day = random.randint(3, 5)  # 3-5 flights per day
            else:  # low
                flights_per_day = random.randint(1, 2)  # 1-2 flights per day
            
            # Generate flights for each day of December
            for day in range(1, 32):  # December 1-31
                flight_date = datetime(2025, 12, day)
                
                # Select which airlines operate this route today
                operating_airlines = random.sample(list(airlines_info.keys()), 
                                                  min(flights_per_day, len(airlines_info)))
                
                # Select time slots for today
                selected_slots = random.sample(departure_slots, 
                                             min(flights_per_day, len(departure_slots)))
                
                for i, airline in enumerate(operating_airlines):
                    if i >= len(selected_slots):
                        break
                        
                    slot = selected_slots[i]
                    airline_data = airlines_info[airline]
                    
                    # Calculate departure and arrival times
                    departure_time = flight_date.replace(
                        hour=slot['hour'],
                        minute=slot['minute']
                    )
                    arrival_time = departure_time + timedelta(hours=duration)
                    
                    # Calculate dynamic pricing
                    price = base_price * airline_data['price_multiplier'] * slot['discount']
                    
                    # Weekend premium (Friday-Sunday)
                    if flight_date.weekday() >= 4:  # Friday = 4, Saturday = 5, Sunday = 6
                        price *= 1.15
                    
                    # Holiday premium (Christmas week: Dec 20-26)
                    if 20 <= day <= 26:
                        price *= 1.25
                    
                    # New Year week premium (Dec 27-31)
                    if 27 <= day <= 31:
                        price *= 1.30
                    
                    # Early bird discount (first week)
                    if 1 <= day <= 7:
                        price *= 0.90
                    
                    # Round to nearest 50
                    final_price = round(price / 50) * 50
                    
                    flight_counter += 1
                    
                    flights_data.append({
                        'flight_id': f'{airline_data["prefix"]}{flight_counter}',
                        'airline': airline,
                        'source': source,
                        'destination': destination,
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'price': final_price
                    })
        
        # Add flights to database in batches for better performance
        print(f"💾 Adding {len(flights_data)} flights to database...")
        batch_size = 100
        for i in range(0, len(flights_data), batch_size):
            batch = flights_data[i:i+batch_size]
            for flight_data in batch:
                flight = Flight(
                    flight_id=flight_data['flight_id'],
                    airline=flight_data['airline'],
                    source=flight_data['source'],
                    destination=flight_data['destination'],
                    departure_time=flight_data['departure_time'],
                    arrival_time=flight_data['arrival_time'],
                    price=flight_data['price'],
                    seats=generate_seats()
                )
                db.session.add(flight)
            
            # Commit each batch
            db.session.commit()
            print(f"   ✓ Added {min(i+batch_size, len(flights_data))}/{len(flights_data)} flights")
        
        print(f"\n✅ Successfully seeded {len(flights_data)} flights for December 2025!")
        
        # Print comprehensive summary
        print(f"\n{'='*60}")
        print(f"📊 DECEMBER 2025 FLIGHT DATABASE SUMMARY")
        print(f"{'='*60}")
        
        # Summary by airline
        print(f"\n✈️  Airlines:")
        airline_counts = {}
        for flight in flights_data:
            airline_counts[flight['airline']] = airline_counts.get(flight['airline'], 0) + 1
        for airline, count in sorted(airline_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {airline}: {count} flights")
        
        # Summary by route
        print(f"\n🛫 Top 15 Routes:")
        route_counts = {}
        for flight in flights_data:
            route = f"{flight['source']} → {flight['destination']}"
            route_counts[route] = route_counts.get(route, 0) + 1
        for i, (route, count) in enumerate(sorted(route_counts.items(), 
                                                   key=lambda x: x[1], reverse=True)[:15], 1):
            print(f"   {i:2d}. {route}: {count} flights")
        
        # Price statistics
        prices = [f['price'] for f in flights_data]
        print(f"\n💰 Pricing:")
        print(f"   Cheapest: ₹{min(prices):,.0f}")
        print(f"   Most Expensive: ₹{max(prices):,.0f}")
        print(f"   Average: ₹{sum(prices)/len(prices):,.0f}")
        
        # Date coverage
        print(f"\n📅 Date Coverage:")
        print(f"   From: December 1, 2025")
        print(f"   To: December 31, 2025")
        print(f"   Total Days: 31 days")
        
        # Cities covered
        cities_covered = set()
        for flight in flights_data:
            cities_covered.add(flight['source'])
            cities_covered.add(flight['destination'])
        print(f"\n🌍 Cities Covered: {len(cities_covered)}")
        print(f"   {', '.join(sorted(cities_covered))}")
        
        print(f"\n{'='*60}")
        print(f"🎉 Database ready for testing!")
        print(f"{'='*60}\n")
        
        # Example searches
        print(f"💡 Try these searches:")
        print(f"   - Mumbai → Delhi, Dec 15")
        print(f"   - Bangalore → Goa, Dec 24 (Christmas)")
        print(f"   - Delhi → Srinagar, Dec 31 (New Year)")
        print(f"   - Chennai → Bangalore, Any day in December\n")

if __name__ == '__main__':
    seed_flights()