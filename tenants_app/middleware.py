# tenants_app/middleware.py
from django.http import JsonResponse
import jwt
from django.conf import settings
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


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.headers.get('Authorization')
        if jwt_token:
            try:
                # Split the token from 'Bearer' space
                token = jwt_token.split(' ')[1]
                # Decode the token with verification
                decoded_token = jwt.decode(
                    token,
                    settings.KEYCLOAK_PUBLIC_KEY,
                    algorithms=["RS256"],
                    audience=settings.JWT_AUDIENCE,
                    options={"verify_signature": True}
                )
                # Set the user information to request
                request.user_id = decoded_token.get('user_id')
                request.user_role = decoded_token.get('role')

                logger.info("JWT decoded successfully with user_id: {} and user_role: {}".format(
                    request.user_id, request.user_role))
            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as e:
                logger.error("JWT validation error: {}".format(str(e)))
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            logger.warning("No JWT found in the request headers")
            return JsonResponse({'error': 'Authorization token not provided'}, status=401)

        response = self.get_response(request)
        return response
    
class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        self.logger.info('Request: %s %s', request.method, request.get_full_path())
        response = self.get_response(request)
        self.logger.info('Response: %s', response.status_code)
        return response
