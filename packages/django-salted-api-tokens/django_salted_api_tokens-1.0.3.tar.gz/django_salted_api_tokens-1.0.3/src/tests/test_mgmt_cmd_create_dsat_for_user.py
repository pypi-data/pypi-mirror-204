import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings

from tests.factories import ApiTokenUserFactory


def call_mgmt_command(cmd: str, *args, **kwargs):
    out, err = StringIO(), StringIO()
    call_command(cmd, *args, stdout=out, stderr=err, **kwargs)
    return out.getvalue()


class TestMgmtCmdCreateDSATForUser(TestCase):
    """
    Tests management command create_dsat_for_user
    """

    def setUp(self) -> None:
        self.user = ApiTokenUserFactory()
        self.cmd = 'create_dsat_for_user'

    def test_non_existing_user(self):
        out = call_mgmt_command(self.cmd, 'non_existing_user')
        self.assertIn('does not exist', out)
        self.assertNotIn('token_id', out)

    def test_existing_user__valid_token_count(self):
        out = call_mgmt_command(self.cmd, self.user)
        resp = json.loads(out)
        for field in ('token_id', 'token', 'message'):
            self.assertIn(field, resp, f'Field {field} is missing in token response')
            self.assertIsNotNone(
                resp[field], f'Field {field} in token response cannot be None'
            )

    def test_view__max_tokens_per_user(self):
        from django.conf import settings

        for i in range(0, settings.DSAT_MAX_TOKENS_PER_USER + 1):
            out = call_mgmt_command(self.cmd, self.user)
            if i >= settings.DSAT_MAX_TOKENS_PER_USER:
                self.assertIn('Maximum tokens limit reached for user', out)
