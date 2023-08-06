from django.urls import path

from django_salted_api_tokens.views import CreateApiToken

app_name = 'django_salted_api_tokens'

urlpatterns = [
    # create django salted api token (dsat)
    path(
        'create-dsat/',
        CreateApiToken.as_view(),
        name='create-dsat',
    ),
]
