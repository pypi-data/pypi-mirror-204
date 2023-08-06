from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import TokenResponseSerializer
from .utils import create_dsat_token_for_user


class CreateApiToken(ObtainAuthToken):
    """
    Create API access token for user.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token_id, user_token = create_dsat_token_for_user(user)
        token_resp = TokenResponseSerializer(
            {'token_id': token_id, 'token': user_token}
        ).data
        return Response(token_resp)
