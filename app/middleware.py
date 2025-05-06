from django.utils.deprecation import MiddlewareMixin
from app.models import UserSession
class CheckUserSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key
        if session_key:
            try:
                user_session = UserSession.objects.get(session_key=session_key)
                if not user_session.is_active:
                    request.session.flush()
                    if request.user.is_authenticated:
                        from django.contrib.auth import logout
                        logout(request)
            except UserSession.DoesNotExist:
                request.session.flush()