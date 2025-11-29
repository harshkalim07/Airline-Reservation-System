from marshmallow import Schema, fields, validate, ValidationError, validates
from datetime import datetime

class FlightCreateSchema(Schema):
    """Schema for creating a new flight"""
    flight_id = fields.Str(required=True, error_messages={
        'required': 'Flight ID is required'
    })
    airline = fields.Str(required=True, validate=validate.Length(min=2), error_messages={
        'required': 'Airline is required'
    })
    source = fields.Str(required=True, validate=validate.Length(min=2), error_messages={
        'required': 'Source is required'
    })
    destination = fields.Str(required=True, validate=validate.Length(min=2), error_messages={
        'required': 'Destination is required'
    })
    departure_time = fields.DateTime(required=True, error_messages={
        'required': 'Departure time is required'
    })
    arrival_time = fields.DateTime(required=True, error_messages={
        'required': 'Arrival time is required'
    })
    price = fields.Float(required=True, validate=validate.Range(min=0), error_messages={
        'required': 'Price is required'
    })
    seats = fields.Dict(keys=fields.Str(), values=fields.Dict())
    
    @validates('destination')
    def validate_destination(self, value):
        if hasattr(self.context.get('data'), 'get'):
            source = self.context.get('data').get('source')
            if source and value == source:
                raise ValidationError('Destination cannot be same as source')

class FlightUpdateSchema(Schema):
    """Schema for updating flight information"""
    airline = fields.Str(validate=validate.Length(min=2))
    source = fields.Str(validate=validate.Length(min=2))
    destination = fields.Str(validate=validate.Length(min=2))
    departure_time = fields.DateTime()
    arrival_time = fields.DateTime()
    price = fields.Float(validate=validate.Range(min=0))
    seats = fields.Dict(keys=fields.Str(), values=fields.Dict())

class FlightSearchSchema(Schema):
    """Schema for searching flights"""
    source = fields.Str(required=True, error_messages={
        'required': 'Source is required'
    })
    destination = fields.Str(required=True, error_messages={
        'required': 'Destination is required'
    })
    date = fields.Date(required=True, error_messages={
        'required': 'Date is required'
    })
    passengers = fields.Int(validate=validate.Range(min=1, max=9), missing=1)

class FlightResponseSchema(Schema):
    """Schema for flight response"""
    id = fields.Str()
    flight_id = fields.Str()
    airline = fields.Str()
    source = fields.Str()
    destination = fields.Str()
    departure_time = fields.DateTime()
    arrival_time = fields.DateTime()
    price = fields.Float()
    available_seats = fields.Int()
    seats = fields.Dict()