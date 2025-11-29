from flask import jsonify
from datetime import datetime

def success_response(data=None, message="Success", status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data (dict, list, or None)
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Flask JSON response
    """
    response = {
        'success': True,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message="An error occurred", errors=None, status_code=400):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        errors: Detailed error information (dict or list)
        status_code: HTTP status code
    
    Returns:
        Flask JSON response
    """
    response = {
        'success': False,
        'error': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if errors is not None:
        response['details'] = errors
    
    return jsonify(response), status_code


def validation_error_response(errors):
    """
    Create a response for validation errors
    
    Args:
        errors: Validation error details (typically from Marshmallow)
    
    Returns:
        Flask JSON response
    """
    return error_response(
        message="Validation failed",
        errors=errors,
        status_code=422
    )


def not_found_response(resource="Resource"):
    """
    Create a 404 not found response
    
    Args:
        resource: Name of the resource not found
    
    Returns:
        Flask JSON response
    """
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )


def unauthorized_response(message="Authentication required"):
    """
    Create a 401 unauthorized response
    
    Args:
        message: Unauthorized message
    
    Returns:
        Flask JSON response
    """
    return error_response(
        message=message,
        status_code=401
    )


def forbidden_response(message="You don't have permission to access this resource"):
    """
    Create a 403 forbidden response
    
    Args:
        message: Forbidden message
    
    Returns:
        Flask JSON response
    """
    return error_response(
        message=message,
        status_code=403
    )


def server_error_response(message="Internal server error"):
    """
    Create a 500 server error response
    
    Args:
        message: Error message
    
    Returns:
        Flask JSON response
    """
    return error_response(
        message=message,
        status_code=500
    )


def paginated_response(items, page, per_page, total_items, message="Success"):
    """
    Create a paginated response
    
    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total_items: Total number of items
        message: Response message
    
    Returns:
        Flask JSON response
    """
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    response = {
        'success': True,
        'message': message,
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return jsonify(response), 200


def created_response(data, message="Resource created successfully"):
    """
    Create a 201 created response
    
    Args:
        data: Created resource data
        message: Success message
    
    Returns:
        Flask JSON response
    """
    return success_response(data=data, message=message, status_code=201)


def no_content_response():
    """
    Create a 204 no content response
    
    Returns:
        Flask JSON response
    """
    return '', 204