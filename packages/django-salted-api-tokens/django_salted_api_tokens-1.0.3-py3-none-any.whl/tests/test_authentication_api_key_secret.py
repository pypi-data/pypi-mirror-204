from ddt import data, ddt, unpack
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from django_salted_api_tokens.authentication import TokenAuthentication
from django_salted_api_tokens.settings import DSAT_X_API_TOKEN_HEADER_NAME
from tests.factories import ApiTokenFactory, ApiTokenUserFactory, test_token


@ddt
class TestTokenAuthentication(TestCase):
    def setUp(self) -> None:
        self.user = ApiTokenUserFactory()
        self.token = ApiTokenFactory(user=self.user)
        self.auth = TokenAuthentication()
        self.token_header = f'HTTP_{DSAT_X_API_TOKEN_HEADER_NAME}'

    data__test_api_token_parsing__invalid_content = (
        # invalid values for authorization header content
        (None, None),
        ('', None),
        ('one_word', None),
        ('two words', None),
        ('with three words', None),
        ('with such four words', None),
        # valid values for authorization header content
        (
            f'{TokenAuthentication.authentication_method} test-token-id test-token',
            'test-token',
        ),
    )

    @data(*data__test_api_token_parsing__invalid_content)
    @unpack
    def test_api_token_parsing__invalid_content(
        self, header_content=None, expected_token=None
    ):
        api_token_id, api_token = self.auth.api_token_from_header(header_content)
        self.assertEqual(
            api_token,
            expected_token,
            f'Parsing failed. Got token {api_token} when expecting {expected_token}',
        )

    def test_api_token__authenticate__valid(self):
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} {self.token.token_id} {test_token}'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        user, auth = TokenAuthentication().authenticate(request)
        self.assertEqual(
            user,
            self.token.user,
            'User did not match expected after authentication',
        )
        self.assertEqual(
            auth,
            None,
            'auth entry did not match expected after authentication',
        )

    def test_api_token__authenticate__revoked_valid(self):
        self.token.revoked = True
        self.token.save()
        self.token.refresh_from_db()
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} {self.token.token_id} {test_token}'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)

    def test_token__authenticate__invalid(self):
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} an_invalid_token_id an_invalid_token'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)

    def test_token__authenticate__invalid_token_id(self):
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} an_invalid_token_id {test_token}'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)

    def test_token__authenticate__invalid_token(self):
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} {self.token.token_id} an_invalid_token'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)

    def test_token__authenticate__revoked_token(self):
        self.token.revoked = True
        self.token.save()
        self.token.refresh_from_db()
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} {self.token.token_id} an_invalid_token'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)

    def test_api_token__authenticate__inactive_user(self):
        self.user.is_active = False
        self.user.save()
        self.user.refresh_from_db()
        factory = APIRequestFactory()
        headers = {
            f'{self.token_header}': f'{self.auth.authentication_method} {self.token.token_id} an_invalid_token'
        }
        request = factory.get('api/commons/languages/', data=None, **headers)
        with self.assertRaises(AuthenticationFailed):
            _ = TokenAuthentication().authenticate(request)
