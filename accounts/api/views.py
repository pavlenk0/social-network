from django.conf import settings
from pyhunter import PyHunter
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.api.serializers import UserSerializer


class CreateUserView(RegisterView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # verify the deliverability of an email address
        hunter = PyHunter(settings.EMAIL_HUNTER_API_KEY)
        verify = hunter.email_verifier(email)
        if not verify['gibberish'] and not verify['block']:
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_response_data(user),
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response({'You use an automatically generated email address '
                         'or your email is blocked'},
                        status=status.HTTP_400_BAD_REQUEST)
