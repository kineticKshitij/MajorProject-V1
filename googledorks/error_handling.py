"""
Robust Error Handling Middleware and Utilities
"""

import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import (
    ValidationError, PermissionDenied, 
    ObjectDoesNotExist, SuspiciousOperation
)
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

logger = logging.getLogger(__name__)


class RobustErrorHandlingMiddleware:
    """
    Middleware to catch and handle all unhandled exceptions gracefully.
    Provides consistent error responses across the application.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.handle_exception(request, e)
    
    def handle_exception(self, request, exception):
        """Handle exceptions and return appropriate JSON response."""
        
        # Log the exception
        logger.error(
            f"Unhandled exception: {type(exception).__name__}",
            exc_info=True,
            extra={
                'path': request.path,
                'method': request.method,
                'user': getattr(request.user, 'username', 'Anonymous')
            }
        )
        
        # Determine status code and message based on exception type
        if isinstance(exception, ObjectDoesNotExist):
            status_code = 404
            message = "The requested resource was not found"
            error_type = "NOT_FOUND"
        
        elif isinstance(exception, ValidationError):
            status_code = 400
            message = str(exception)
            error_type = "VALIDATION_ERROR"
        
        elif isinstance(exception, PermissionDenied):
            status_code = 403
            message = "You don't have permission to access this resource"
            error_type = "PERMISSION_DENIED"
        
        elif isinstance(exception, SuspiciousOperation):
            status_code = 400
            message = "Suspicious operation detected"
            error_type = "SUSPICIOUS_OPERATION"
        
        else:
            status_code = 500
            message = "An unexpected error occurred. Please try again later."
            error_type = "INTERNAL_ERROR"
        
        # Build error response
        error_response = {
            'success': False,
            'error': {
                'type': error_type,
                'message': message,
                'code': status_code
            }
        }
        
        # Add debug info in development
        from django.conf import settings
        if settings.DEBUG:
            error_response['error']['debug'] = {
                'exception': type(exception).__name__,
                'details': str(exception),
                'traceback': traceback.format_exc()
            }
        
        return JsonResponse(
            error_response,
            status=status_code,
            safe=False
        )


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework.
    Provides consistent error response format.
    """
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, DRF didn't handle it
    if response is None:
        logger.error(
            f"Unhandled DRF exception: {type(exc).__name__}",
            exc_info=True,
            extra={
                'view': context.get('view').__class__.__name__,
                'request': context.get('request').path
            }
        )
        
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred',
                    'code': 500
                }
            },
            status=500
        )
    
    # Customize the response format
    if hasattr(response, 'data'):
        error_data = {
            'success': False,
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': response.status_code
            }
        }
        
        # Add field-specific errors if present
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['error']['details'] = response.data['detail']
            else:
                error_data['error']['fields'] = response.data
        
        response.data = error_data
    
    return response


class APIErrorResponse:
    """
    Helper class to create consistent error responses in views.
    """
    
    @staticmethod
    def not_found(message="Resource not found", details=None):
        """Return a 404 error response."""
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'NOT_FOUND',
                    'message': message,
                    'details': details,
                    'code': 404
                }
            },
            status=404
        )
    
    @staticmethod
    def bad_request(message="Invalid request", details=None):
        """Return a 400 error response."""
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'BAD_REQUEST',
                    'message': message,
                    'details': details,
                    'code': 400
                }
            },
            status=400
        )
    
    @staticmethod
    def unauthorized(message="Authentication required"):
        """Return a 401 error response."""
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'UNAUTHORIZED',
                    'message': message,
                    'code': 401
                }
            },
            status=401
        )
    
    @staticmethod
    def forbidden(message="Permission denied"):
        """Return a 403 error response."""
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'FORBIDDEN',
                    'message': message,
                    'code': 403
                }
            },
            status=403
        )
    
    @staticmethod
    def server_error(message="Internal server error", details=None):
        """Return a 500 error response."""
        return JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'INTERNAL_ERROR',
                    'message': message,
                    'details': details,
                    'code': 500
                }
            },
            status=500
        )
    
    @staticmethod
    def rate_limited(message="Too many requests", retry_after=None):
        """Return a 429 error response."""
        response = JsonResponse(
            {
                'success': False,
                'error': {
                    'type': 'RATE_LIMITED',
                    'message': message,
                    'code': 429
                }
            },
            status=429
        )
        
        if retry_after:
            response['Retry-After'] = retry_after
        
        return response


def safe_api_call(func):
    """
    Decorator to wrap API view functions with error handling.
    Usage:
        @safe_api_call
        def my_view(request):
            # Your code here
    """
    def wrapper(*args, **kwargs):
        from django.conf import settings
        
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist as e:
            logger.warning(f"Resource not found in {func.__name__}: {e}")
            return APIErrorResponse.not_found(str(e))
        
        except ValidationError as e:
            logger.warning(f"Validation error in {func.__name__}: {e}")
            return APIErrorResponse.bad_request(
                message="Validation failed",
                details=e.message_dict if hasattr(e, 'message_dict') else str(e)
            )
        
        except PermissionDenied as e:
            logger.warning(f"Permission denied in {func.__name__}: {e}")
            return APIErrorResponse.forbidden(str(e))
        
        except Exception as e:
            logger.error(
                f"Unexpected error in {func.__name__}: {e}",
                exc_info=True
            )
            return APIErrorResponse.server_error(
                message="An unexpected error occurred",
                details=str(e) if settings.DEBUG else None
            )
    
    return wrapper


# Common error messages
ERROR_MESSAGES = {
    'DORK_NOT_FOUND': 'The requested dork does not exist',
    'ENTITY_NOT_FOUND': 'The requested entity does not exist',
    'INVALID_QUERY': 'Invalid search query provided',
    'EXECUTION_FAILED': 'Failed to execute the dork search',
    'CRAWLER_ERROR': 'Crawler operation failed',
    'PROFILE_NOT_FOUND': 'Profile not found',
    'JOB_NOT_FOUND': 'Crawl job not found',
    'SCHEDULE_NOT_FOUND': 'Schedule not found',
    'UNAUTHORIZED': 'You must be logged in to perform this action',
    'FORBIDDEN': 'You do not have permission to perform this action',
    'RATE_LIMIT': 'Too many requests. Please slow down.',
    'INVALID_DATA': 'Invalid data provided in the request',
}


class DorkExecutionException(APIException):
    """Custom exception for dork execution failures."""
    status_code = 500
    default_detail = 'Failed to execute dork search'
    default_code = 'dork_execution_failed'


class CrawlerException(APIException):
    """Custom exception for crawler operation failures."""
    status_code = 500
    default_detail = 'Crawler operation failed'
    default_code = 'crawler_failed'


class BreachCheckerException(APIException):
    """Custom exception for breach checker failures."""
    status_code = 500
    default_detail = 'Breach check operation failed'
    default_code = 'breach_check_failed'
