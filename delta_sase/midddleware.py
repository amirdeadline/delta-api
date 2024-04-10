import logging

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        self.logger.info('Request: %s %s', request.method, request.get_full_path())
        response = self.get_response(request)
        self.logger.info('Response: %s', response.status_code)
        return response