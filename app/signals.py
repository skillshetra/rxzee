from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from app.models import UserSession
from django.utils.timezone import now
from json import loads as load_data

@receiver(user_logged_in)
def user_logged_in_handler(request, user, **kwargs):
    session_data = request.POST.get('session_data', '')
    ip_address = ''
    country = ''
    region = ''
    city = ''
    zip_code = ''
    if session_data:
        session_data = load_data(session_data)
        ip_address = session_data['query']
        country = session_data['country']
        region = session_data['regionName']
        city = session_data['city']
        zip_code = session_data['zip']
    UserSession.objects.update_or_create(session_key = request.session.session_key, defaults = {'ip_address': ip_address, 'country': country, 'region': region, 'city': city, 'zip_code': zip_code, 'user': user, 'user_agent': request.META.get('HTTP_USER_AGENT', '')})

@receiver(user_logged_out)
def user_logged_out_handler(request, user, **kwargs):
    try:
        user_session = UserSession.objects.get(session_key = request.session.session_key, user = user)
        user_session.session_expiration = now()
        user_session.is_active = False
        user_session.save()
    except UserSession.DoesNotExist:
        pass