from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def validate(self, attrs):
        validate_password(attrs.get('password'))
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('password and  confirm password do not match'))

        return attrs


class ChangeUserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        validate_password(attrs.get('new_password'))
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('password and  confirm password do not match'))

        return attrs

    def update(self, instance, validated_data):
        if instance.check_passwrod(validated_data.get('current_password')):
            instance.password = make_password(validated_data.get('new_password'))
            instance.save()
            return instance
        return serializers.ValidationError(_('password is incorrect'))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'is_active')
        read_only_fields = ('id', 'date_joined', 'is_active')