import random
import string
from datetime import datetime

def generate_pnr():
    """
    Generate a unique PNR (Passenger Name Record) number
    
    Format: 2-letter prefix + 4 digits + 2 random uppercase letters
    Example: FL3456AB, AI7890XY
    
    Returns:
        String: Generated PNR
    """
    # Airline prefix (you can customize this)
    prefix = random.choice(['FL', 'AI', 'IN', 'UK', 'SG', 'DE'])
    
    # 4 random digits
    digits = ''.join(random.choices(string.digits, k=4))
    
    # 2 random uppercase letters
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    pnr = f"{prefix}{digits}{letters}"
    
    return pnr


def generate_pnr_with_timestamp():
    """
    Generate a PNR with timestamp embedded
    
    Format: YYMMDD + 4 random alphanumeric characters
    Example: 2311251A2B (for Nov 25, 2023)
    
    Returns:
        String: Generated PNR with timestamp
    """
    # Get current date in YYMMDD format
    timestamp = datetime.utcnow().strftime('%y%m%d')
    
    # 4 random alphanumeric characters
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    pnr = f"{timestamp}{random_chars}"
    
    return pnr


def validate_pnr_format(pnr):
    """
    Validate PNR format
    
    Args:
        pnr: PNR string to validate
    
    Returns:
        Boolean: True if valid format, False otherwise
    """
    if not pnr or not isinstance(pnr, str):
        return False
    
    # Check length (should be 8 characters)
    if len(pnr) != 8:
        return False
    
    # Check format: 2 letters + 4 digits + 2 letters
    if not (pnr[:2].isalpha() and 
            pnr[2:6].isdigit() and 
            pnr[6:].isalpha()):
        return False
    
    return True


def generate_booking_reference(airline_code='FL'):
    """
    Generate a booking reference number
    
    Args:
        airline_code: 2-letter airline code (default: FL)
    
    Returns:
        String: Generated booking reference
    """
    # Format: AIRLINE-YYYYMMDD-XXXX
    date_str = datetime.utcnow().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    return f"{airline_code}-{date_str}-{random_str}"