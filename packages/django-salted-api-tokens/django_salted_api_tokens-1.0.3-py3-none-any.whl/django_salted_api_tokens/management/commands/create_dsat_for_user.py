import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.exceptions import ValidationError

from django_salted_api_tokens.serializers import TokenResponseSerializer
from django_salted_api_tokens.utils import create_dsat_token_for_user

user_model = get_user_model()


class Command(BaseCommand):
    help = "Create a DSAT token for user"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        try:
            user = user_model.objects.get(username=username)
            token_id, user_token = create_dsat_token_for_user(user)
            token_resp = TokenResponseSerializer(
                {'token_id': token_id, 'token': user_token}
            ).data
            self.stdout.write(self.style.SUCCESS(json.dumps(token_resp)))
        except ValidationError as ve:
            self.stdout.write(self.style.ERROR(f'{ve}'))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Username {username} does not exist'))
