from social_auth.exceptions import AuthFailed
from django.conf import settings


def check_credentials(details, user=None, *args, **kwargs):
    """Check that user is a lateral-thoughts member."""
    if user:
        return None

    email = details.get('email')

    if not email or not email.endswith(settings.AGORA_ORGANIZATION_DOMAIN):
        raise AuthFailed(kwargs['backend'], 'You must connect with your %s account.' % settings.AGORA_ORGANIZATION_NAME)
    return None
