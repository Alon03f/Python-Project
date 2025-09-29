from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for better error responses"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            "error": True,
            "message": "An error occurred",
            "details": response.data
        }
        
        if isinstance(exc, ValidationError):
            custom_response_data["message"] = "Validation error"
        elif isinstance(exc, IntegrityError):
            custom_response_data["message"] = "Database integrity error"
            
        response.data = custom_response_data
        logger.error(f"API Error: {exc}", exc_info=True)
    else:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        response = Response(
            {
                "error": True,
                "message": "An unexpected error occurred",
                "details": str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


def sanitize_html(content):
    """Sanitize HTML content to prevent XSS attacks"""
    import bleach
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'
    ]
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title', 'width', 'height']
    }
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes, strip=True)