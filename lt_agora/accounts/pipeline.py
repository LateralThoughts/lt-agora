from social_auth.exceptions import AuthFailed


def check_credentials(details, user=None, *args, **kwargs):
    """Check that user is a lateral-thoughts member."""
    if user:
        return None

    email = details.get('email')

    if not email or not email.endswith("@lateral-thoughts.com"):
        raise AuthFailed(kwargs['backend'], 'You must connect with your Lateral Thoughts account.')
    return None
