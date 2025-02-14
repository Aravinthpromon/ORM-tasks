# import base64
# from django.http import JsonResponse
# from django.utils.deprecation import MiddlewareMixin


# class BasicAuthMiddleware(MiddlewareMixin):
#     VALID_USERNAME = "admin"
#     VALID_PASSWORD = "123"

#     def process_request(self, request):
#         auth_header = request.headers.get('Authorization')

#         if request.path == '/' or request.path.startswith("/admin/"):
#             return None

#         if not auth_header or not auth_header.startswith('Basic '):
#             return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

#         encoded_credentials = auth_header.split(' ')[1]
#         decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
#         username, password = decoded_credentials.split(':')

#         if username != self.VALID_USERNAME or password != self.VALID_PASSWORD:
#             return JsonResponse({"error": "Invalid username or password"}, status=401)
##########################################################
# import base64
# import os
# from django.http import JsonResponse
# from django.utils.deprecation import MiddlewareMixin
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# import logging

# logger = logging.getLogger(__name__)

# def process_request(self, request):
#     auth_header = request.headers.get('Authorization')
#     logger.info(f"DEBUG: Received Auth Header -> {auth_header}")  # Debugging

#     if not auth_header or not auth_header.startswith('Basic '):
#         return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)


# class BasicAuthMiddleware(MiddlewareMixin):
#     VALID_USERNAME = os.getenv("AUTH_USERNAME", "admin")  # Default to "admin" if not set
#     VALID_PASSWORD = os.getenv("AUTH_PASSWORD", "123")    # Default to "123" if not set

#     def process_request(self, request):
#         auth_header = request.headers.get('Authorization')

#         if request.path == '/' or request.path.startswith("/admin/"):
#             return None  # Skip authentication for home and admin pages

#         if not auth_header or not auth_header.startswith('Basic '):
#             return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

#         encoded_credentials = auth_header.split(' ')[1]
#         decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
#         username, password = decoded_credentials.split(':')

#         if username != self.VALID_USERNAME or password != self.VALID_PASSWORD:
#             return JsonResponse({"error": "Invalid username or password"}, status=401)
        
        #########################################################################
# import logging
# import base64
# from django.http import JsonResponse
# from django.utils.deprecation import MiddlewareMixin

# logger = logging.getLogger(__name__)

# class BasicAuthMiddleware(MiddlewareMixin):
#     """Middleware for Basic Authentication"""

#     def process_request(self, request):
#         auth_header = request.headers.get('Authorization')
#         logger.info(f"DEBUG: Received Auth Header -> {auth_header}")  # Debugging

#         if not auth_header or not auth_header.startswith('Basic '):
#             logger.warning("Unauthorized: Missing or invalid Authorization header")
#             return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

#         try:
#             encoded_credentials = auth_header.split(' ')[1]
#             decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
#             username, password = decoded_credentials.split(':')
#             logger.info(f"DEBUG: Decoded Credentials -> Username: {username}, Password: {password}")  # Debugging
#         except Exception as e:
#             logger.error(f"ERROR: Failed to decode credentials -> {e}")
#             return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

#         if username != "admin" or password != "123":
#             logger.warning("Unauthorized: Invalid username or password")
#             return JsonResponse({"error": "Invalid username or password"}, status=401)


import logging
import base64
import os
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class BasicAuthMiddleware(MiddlewareMixin):
    """Middleware for Basic Authentication"""

    VALID_USERNAME = os.getenv("AUTH_USERNAME", "admin")
    VALID_PASSWORD = os.getenv("AUTH_PASSWORD", "123")

    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        logger.info(f"DEBUG: Received Auth Header -> {auth_header}")  # Debugging

        if not auth_header or not auth_header.startswith('Basic '):
            logger.warning("Unauthorized: Missing or invalid Authorization header")
            return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

        try:
            encoded_credentials = auth_header.split(' ')[1]
            # raise ValueError("This is a forced error for testing")
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':')
            logger.info(f"DEBUG: Decoded Credentials -> Username: {username}, Password: {password}")  # Debugging
        except Exception as e:
            logger.error(f"ERROR: Failed to decode credentials -> {e}")
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        if username != self.VALID_USERNAME or password != self.VALID_PASSWORD:
            logger.warning("Unauthorized: Invalid username or password")
            return JsonResponse({"error": "Invalid username or password"}, status=401)

