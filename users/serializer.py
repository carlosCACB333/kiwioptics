from rest_framework import serializers

class LoginSocialSerializer(serializers.Serializer):
    token_id=serializers.CharField(required=True)

class LoginSocialSerializer2(serializers.Serializer):
    token_id=serializers.CharField(required=True)
    optic=serializers.CharField(required=True)
