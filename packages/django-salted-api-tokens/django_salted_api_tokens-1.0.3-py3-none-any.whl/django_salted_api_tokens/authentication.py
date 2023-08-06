from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from django_salted_api_tokens.models import ApiToken
from django_salted_api_tokens.utils import verify_hashed_secret


class TokenAuthentication(authentication.BaseAuthentication):
    authentication_method = 'token'

    def api_token_from_header(self, content):
        if not content:
            return None, None
        try:
            auth_method, api_token_id, api_token = content.split()
            if (
                not auth_method
                or not api_token_id
                or not api_token
                or auth_method.lower() != self.__class__.authentication_method
            ):
                return None, None
            return api_token_id, api_token
        except (AttributeError, ValueError):
            return None, None

    def authenticate(self, request):
        request_meta = request.META
        hdr_token = request_meta.get('HTTP_AUTHORIZATION')

        if not hdr_token:
            return None

        in_token_id, in_token = self.api_token_from_header(hdr_token)
        if not in_token or not in_token_id:
            return None

        db_token = ApiToken.objects.filter(token_id=in_token_id).first()
        if not db_token or db_token.revoked:
            raise AuthenticationFailed('Invalid token')

        if not db_token.user.is_active:
            raise AuthenticationFailed('User is inactive')

        verified = verify_hashed_secret(in_token, db_token.token)
        if not verified:
            raise AuthenticationFailed('Token verification failed')

        return db_token.user, None
