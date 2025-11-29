from marshmallow import Schema, fields, validate, ValidationError

class UserRegistrationSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True, error_messages={
        'required': 'Email is required',
        'invalid': 'Invalid email format'
    })
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, error='Password must be at least 6 characters long'),
        error_messages={'required': 'Password is required'}
    )
    role = fields.Str(
        missing='user',
        validate=validate.OneOf(['user', 'admin']),
        error_messages={'validator_failed': 'Role must be either user or admin'}
    )

class UserLoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True, error_messages={
        'required': 'Email is required',
        'invalid': 'Invalid email format'
    })
    password = fields.Str(required=True, error_messages={
        'required': 'Password is required'
    })

class UserUpdateSchema(Schema):
    """Schema for updating user information"""
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(['user', 'admin']))

class UserResponseSchema(Schema):
    """Schema for user response"""
    id = fields.Int()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.DateTime()