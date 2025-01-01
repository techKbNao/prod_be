import os

from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.auth import FirebaseAuthSerializer

user_model = get_user_model()


# signup
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    """
    bodyの中のtokenを検証してユーザーを作成
    """
    print(request.data)
    serializer = FirebaseAuthSerializer(data=request.data)
    # 値の検証
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = serializer.validated_data["token"]
    try:
        # Firebase Admin SDKでトークンを検証
        decoded_token = auth.verify_id_token(token)

    except auth.ExpiredIdTokenError:
        return Response({"detail": "Token has been expired."}, status=status.HTTP_401_UNAUTHORIZED)
    except auth.RevokedIdTokenError:
        return Response({"detail": "Token has been revoked."}, status=status.HTTP_401_UNAUTHORIZED)
    except auth.InvalidIdTokenError:
        return Response({"detail": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)

    email, firebase_uid = decoded_token.get("email"), decoded_token.get("uid")

    if user_model.objects.filter(firebase_uid=firebase_uid).exists():
        return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # ユーザーの作成
    user = user_model.objects.create(username=email, email=email, firebase_uid=firebase_uid)
    # パスワードの無効化
    user.set_unusable_password()
    user.save()

    return Response({"detail": "Successfully created"}, status=status.HTTP_201_CREATED)


# NOTE:認証はAuthenticationBackendを使ってMiddlewareが行うべき
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    送られてきたTokenを検証してCookieに入れる
    """
    # リクエストから送信されたトークンを取得
    serializer = FirebaseAuthSerializer(data=request.data)
    # 値の検証
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = serializer.validated_data["token"]
    try:
        # Firebase Admin SDKでトークンを検証
        auth.verify_id_token(token)
        response = Response({"message": "Toke was successfully saved!!!"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=os.getenv("AUTH_TOKEN_KEY"),
            value=token,
            httponly=True,
            secure=True,  # HTTPS通信でのみ送信(開発時はhttpでよい)
            samesite="None",
            max_age=3600 * 24 * 7,
            path="/",
        )
        return response
    except auth.ExpiredIdTokenError:
        return Response({"detail": "Token has been expired."}, status=status.HTTP_401_UNAUTHORIZED)
    except auth.RevokedIdTokenError:
        return Response({"detail": "Token has been revoked."}, status=status.HTTP_401_UNAUTHORIZED)
    except auth.InvalidIdTokenError:
        return Response({"detail": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def basic_view(request):
    """
    テスト用のエンドポイントなので、消すけす。
    """
    return Response({"detail": request.user.email}, status=status.HTTP_200_OK)
