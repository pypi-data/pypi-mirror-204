import hashlib
import secrets

from ksuid import ksuid
from rest_framework.exceptions import ValidationError

from django_salted_api_tokens.models import ApiToken
from django_salted_api_tokens.settings import (
    DSAT_HASHLIB_ALGO,
    DSAT_MAX_TOKENS_PER_USER,
    DSAT_TOKEN_LENGTH,
)

hashers = {
    'sha512': hashlib.sha512,
    'sha384': hashlib.sha384,
    'sha256': hashlib.sha256,
}


def gen_token(n_chars=40):
    return secrets.token_hex(int(n_chars / 2))


def hashed_secret(secret: str, algo: str, salt: str = None):
    if not salt:
        salt = secrets.token_hex(24)
    hash_func = hashers.get(algo, None)
    if not hash_func:
        raise ValueError(
            f'Unsupported hash algorithm {algo}. Check DSAT_HASHLIB_ALGO in settings.py'
        )
    m = hash_func()
    m.update(f'{secret}_{salt}'.encode())
    return f'{m.hexdigest()}${salt}${algo}'


def verify_hashed_secret(secret, encoded):
    hash_orig, salt, algo = encoded.split('$')
    hashed = hashed_secret(secret, algo, salt)
    return encoded == hashed


def create_dsat_token_for_user(user):
    n_user_tokens = ApiToken.objects.filter(user=user).count()
    if n_user_tokens >= DSAT_MAX_TOKENS_PER_USER:
        raise ValidationError('Maximum tokens limit reached for user')
    token_id, user_token = f'{ksuid()}', gen_token(n_chars=DSAT_TOKEN_LENGTH)
    db_token, created = ApiToken.objects.get_or_create(
        user=user,
        token_id=token_id,
        token=hashed_secret(secret=user_token, algo=DSAT_HASHLIB_ALGO),
    )
    return db_token.token_id, user_token
