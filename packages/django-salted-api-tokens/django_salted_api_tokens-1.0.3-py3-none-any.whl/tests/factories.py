import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from factory import lazy_attribute
from factory.django import DjangoModelFactory
from ksuid import ksuid

from django_salted_api_tokens.models import ApiToken
from django_salted_api_tokens.utils import gen_token, hashed_secret

user_model = get_user_model()
test_password = gen_token(n_chars=12)
test_token_id = f'{ksuid()}'
test_token = gen_token()
test_hashlib_algo = 'sha512'


@factory.django.mute_signals(post_save)
class SuperUserFactory(DjangoModelFactory):
    class Meta:
        model = user_model

    username = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password(test_password))
    is_staff = True
    is_active = True
    is_superuser = True


@factory.django.mute_signals(post_save)
class ApiTokenUserFactory(DjangoModelFactory):
    class Meta:
        model = user_model

    username = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password(test_password))
    is_staff = False
    is_active = True
    is_superuser = False


class ApiTokenFactory(DjangoModelFactory):
    class Meta:
        model = ApiToken

    user = factory.SubFactory(SuperUserFactory)
    token_id = test_token_id
    token = lazy_attribute(lambda k: hashed_secret(test_token, test_hashlib_algo))
    revoked = False
