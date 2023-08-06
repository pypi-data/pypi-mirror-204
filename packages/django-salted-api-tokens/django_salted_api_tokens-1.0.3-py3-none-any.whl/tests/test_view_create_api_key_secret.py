from http import HTTPStatus

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from tests.factories import ApiTokenUserFactory, test_password


class TestViewCreateApiToken(TestCase):
    def setUp(self) -> None:
        self.user = ApiTokenUserFactory()
        self.url_dsat = '/dsat/create-dsat/'

    def _assert_http_ok_token_reponse(self, response):
        self.assertEqual(
            HTTPStatus.OK, response.status_code, 'Invalid status on getting token'
        )
        for item in (
            'token_id',
            'token',
            'message',
        ):
            self.assertIn(item, response.data, f'item {item} missing in response')
            self.assertTrue(response.data[item], f'item {item} is empty in response')

    def test_view__create_api_token(self):
        client = APIClient(enforce_csrf_checks=True)
        ep = self.url_dsat
        data = {'username': self.user.username, 'password': test_password}
        response = client.post(path=ep, data=data)
        self._assert_http_ok_token_reponse(response)

    def test_view__max_tokens_per_user(self):
        from django.conf import settings

        for i in range(0, settings.DSAT_MAX_TOKENS_PER_USER + 1):
            client = APIClient(enforce_csrf_checks=True)
            ep = self.url_dsat
            data = {'username': self.user.username, 'password': test_password}
            if i < settings.DSAT_MAX_TOKENS_PER_USER:
                response = client.post(path=ep, data=data)
                self._assert_http_ok_token_reponse(response)
            else:
                response = client.post(path=ep, data=data)
                self.assertEqual(
                    HTTPStatus.BAD_REQUEST,
                    response.status_code,
                    'Validation error must be raised on reaching DSAT_MAX_TOKENS_PER_USER',
                )
