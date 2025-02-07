import base64
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class BasicAuthMiddleware(MiddlewareMixin):
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "123"

    def process_request(self, request):
        auth_header = request.headers.get('Authorization')

        if request.path == '/' or request.path.startswith("/admin/"):
            return None

        if not auth_header or not auth_header.startswith('Basic '):
            return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')

        if username != self.VALID_USERNAME or password != self.VALID_PASSWORD:
            return JsonResponse({"error": "Invalid username or password"}, status=401)