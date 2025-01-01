from django.contrib.auth import get_user_model
from rest_framework import serializers

# 認証用のモデルの取得
user_model = get_user_model()


class FirebaseAuthSerializer(serializers.Serializer):
    """
    Firebase認証用のシリアライザー
    """

    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        """
        tokenフィールドの検証
        """
        if not value:
            raise serializers.ValidationError("Token is required.")
        return value
