from django.conf import settings

TWITTER_C_KEY = getattr(settings, 'TWITTER_C_KEY', None)
TWITTER_C_SECRET = getattr(settings, 'TWITTER_C_SECRET', None)
TWITTER_A_TOKEN = getattr(settings, 'TWITTER_A_TOKEN', None)
TWITTER_A_TOKEN_SECRET = getattr(settings, 'TWITTER_A_TOKEN_SECRET', None)