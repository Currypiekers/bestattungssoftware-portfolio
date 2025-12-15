from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context, get_tenant_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            header = auth.get_header(request)
            if header is not None:
                raw_token = auth.get_raw_token(header)
                if raw_token is not None:
                    validated_token = auth.get_validated_token(raw_token)
                    user = auth.get_user(validated_token)  # Get the user from the token

                    # Now you can securely access the company through the user object
                    if user and hasattr(user, 'company') and user.company:
                        company_name = user.company.schema_name  # Use schema_name instead of name
                        with schema_context(company_name):
                            request.tenant = user.company
        except (InvalidToken, AuthenticationFailed) as e:
            # Handle invalid tokens (log, return an error response, etc.)
            print(f"Invalid token: {e}")
            pass  # Or raise an exception if you want to block the request

# filepath: /root/coverM/app/users/middleware.py
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from datetime import datetime

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        now = timezone.now()
        last_activity_str = request.session.get('last_activity', None)

        # Convert last_activity back to a datetime object if it exists
        if last_activity_str:
            try:
                last_activity = datetime.fromisoformat(last_activity_str)
            except ValueError:
                last_activity = now  # In case of a parsing error, default to now
        else:
            last_activity = now

        # Check if inactivity time has exceeded the AUTO_LOGOUT_DELAY
        if (now - last_activity).total_seconds() > settings.AUTO_LOGOUT_DELAY:
            # Attempt to blacklist the refresh token from the Authorization header
            auth = JWTAuthentication()
            try:
                header = auth.get_header(request)
                if header is not None:
                    raw_token = auth.get_raw_token(header)
                    if raw_token is not None:
                        # Assuming the token is an access token, find the corresponding refresh token
                        try:
                            access_token = AccessToken(raw_token)
                            refresh_token_value = access_token.payload.get('refresh_token')
                            if refresh_token_value:
                                refresh_token = RefreshToken(refresh_token_value)
                                refresh_token.blacklist()
                        except Exception as e:
                            print(f"Could not blacklist token: {e}")
            except Exception as e:
                print(f"Authentication error: {e}")

            request.session.flush()  # Clear session data
        else:
            request.session['last_activity'] = now.isoformat()  # Store 'last_activity' as an ISO string