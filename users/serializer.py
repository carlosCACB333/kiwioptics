from rest_framework import serializers

from .models import Account

class LoginSocialSerializer(serializers.Serializer):
    token_id=serializers.CharField(required=True)

class LoginSocialSerializer2(serializers.Serializer):
    token_id=serializers.CharField(required=True)
    optic=serializers.CharField(required=True)

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=("picture",)

