from rest_framework import serializers

from app.models import UserPasswordManager


class UserNameAplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPasswordManager
        fields = ('name', 'application_type')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserPasswordManager
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = UserPasswordManager(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
