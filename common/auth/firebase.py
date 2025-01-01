from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import authentication

User = get_user_model()


class FirebaseCookieAuthentication(authentication.BaseAuthentication):
    """
    クッキーからFirebaseトークンを取得して認証を行うカスタム認証クラス
    """

    def authenticate(self, request):
        # クッキーからトークンを取得
        cookie_name = "token"  # トークンが保存されているクッキー名
        token = request.COOKIES.get(cookie_name)
        firebase_uid = ""
        if not token:
            return None  # トークンがない場合は認証をスキップ

        try:
            # Firebaseでトークンを検証
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token.get("uid")
        except auth.InvalidIdTokenError:
            return None

        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            return None

        return (user, None)
