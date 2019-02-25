from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from accounts.models import User


class UserSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    phone_number = serializers.CharField()
    date_of_birth = serializers.DateField()
    address = serializers.CharField()

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'address': self.validated_data.get('address', ''),
            'password1': self.validated_data.get('password1', '')
        }

    def save(self, request):
        """
        Override save method to save custom fields:
        address, phone_number, date_of_birth
        """
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.address = self.cleaned_data.get('address')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
