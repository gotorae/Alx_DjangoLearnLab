# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email", "username", "first_name", "last_name",
            "bio", "profile_picture",
            "password", "password_confirmation",
        ]

    def validate(self, attrs):
        # confirm match
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError({"password_confirmation": "Passwords do not match"})
        pwd = attrs["password"]
        # basic strength rules (tune as you prefer)
        if not re.search(r"[A-Z]", pwd):
            raise serializers.ValidationError({"password": "Must contain at least one uppercase letter"})
        if not re.search(r"[a-z]", pwd):
            raise serializers.ValidationError({"password": "Must contain at least one lowercase letter"})
        if not re.search(r"\d", pwd):
            raise serializers.ValidationError({"password": "Must contain at least one digit"})
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            raise serializers.ValidationError({"password": "Must contain at least one special character"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "first_name", "last_name", "bio", "profile_picture"]
        read_only_fields = ["email"]

