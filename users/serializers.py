from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import Favorite


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField()
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    @staticmethod
    def validate_username(username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        return ValidationError('User already exist!')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'),
                                   password=validated_data.get('password'), email=validated_data.get('email'))
        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4)
    password = serializers.CharField()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'