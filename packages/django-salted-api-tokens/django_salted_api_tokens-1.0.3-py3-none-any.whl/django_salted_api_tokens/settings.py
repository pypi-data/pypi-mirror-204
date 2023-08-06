from django.conf import settings

# API Key Secret Authentication settings
# Internal app settings
DSAT_X_API_TOKEN_HEADER_NAME = 'AUTHORIZATION'
DSAT_TOKEN_ID_LENGTH = 40

# Configurable settings from Django project
DSAT_TOKEN_LENGTH = getattr(settings, 'DSAT_TOKEN_LENGTH', 80)
DSAT_MAX_TOKENS_PER_USER = getattr(settings, 'DSAT_MAX_TOKENS_PER_USER', 10)
DSAT_HASHLIB_ALGO = getattr(settings, 'DSAT_HASHLIB_ALGO', 'sha512')
