# base/middleware.py

from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"Unhandled exception occurred: {str(exception)}", exc_info=True)
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(exception)
        }, status=500)
