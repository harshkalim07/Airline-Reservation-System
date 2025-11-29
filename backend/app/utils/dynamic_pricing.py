def calculate_dynamic_price(flight, seat_class='economy'):
    """Calculate dynamic price based on seat availability"""
    base_price = flight.price
    available_seats = len(flight.get_available_seats())
    total_seats = len(flight.seats)
    
    # Calculate occupancy rate
    occupancy = (total_seats - available_seats) / total_seats
    
    # Price multiplier based on occupancy
    if occupancy > 0.8:  # More than 80% booked
        multiplier = 1.5
    elif occupancy > 0.5:  # More than 50% booked
        multiplier = 1.2
    else:
        multiplier = 1.0
    
    # Seat class multiplier
    class_multipliers = {
        'economy': 1.0,
        'business': 2.0,
        'first': 3.0
    }
    
    final_price = base_price * multiplier * class_multipliers.get(seat_class, 1.0)
    
    return round(final_price, 2)