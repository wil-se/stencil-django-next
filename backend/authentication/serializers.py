from rest_framework import serializers
from .models import UserData
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authentication.models import UserData, NonceSignRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "address", "password", "role"]

    def create(self, validated_data):
        user = UserData.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        role = self.user.role.replace('(', '').replace(')', '').split(',')[0].replace('\'', '').lower()
        return {'data': data, 'role': role, 'id': self.user.id}



class NonceSignRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonceSignRequest
        fields = [
            'address',
            'nonce',
            'user'
            ]
