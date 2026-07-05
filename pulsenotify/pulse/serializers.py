from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PriceAlert

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

from .models import PriceAlert


class PriceAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceAlert

        fields = [
            "id",
            "origin",
            "destination",
            "threshold_price",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]