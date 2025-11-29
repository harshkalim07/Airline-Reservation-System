from marshmallow import Schema, fields, validate, ValidationError

class BookingCreateSchema(Schema):
    """Schema for creating a new booking"""
    flight_id = fields.Str(required=True, error_messages={
        'required': 'Flight ID is required'
    })
    passenger_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=200),
        error_messages={'required': 'Passenger name is required'}
    )
    seat_number = fields.Str(required=True, error_messages={
        'required': 'Seat number is required'
    })
    payment_status = fields.Str(
        missing='completed',
        validate=validate.OneOf(['pending', 'completed', 'failed'])
    )

class BookingUpdateSchema(Schema):
    """Schema for updating booking information"""
    passenger_name = fields.Str(validate=validate.Length(min=2, max=200))
    seat_number = fields.Str()
    status = fields.Str(validate=validate.OneOf(['confirmed', 'cancelled']))
    payment_status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))

class BookingCancelSchema(Schema):
    """Schema for cancelling a booking"""
    reason = fields.Str(validate=validate.Length(max=500))

class BookingResponseSchema(Schema):
    """Schema for booking response"""
    id = fields.Int()
    pnr = fields.Str()
    flight_id = fields.Str()
    passenger_name = fields.Str()
    seat_number = fields.Str()
    status = fields.Str()
    payment_status = fields.Str()
    booking_date = fields.DateTime()
    created_at = fields.DateTime()

class BookingSearchSchema(Schema):
    """Schema for searching bookings"""
    pnr = fields.Str()
    email = fields.Email()
    status = fields.Str(validate=validate.OneOf(['confirmed', 'cancelled']))
    start_date = fields.Date()
    end_date = fields.Date()