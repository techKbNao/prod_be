from django.urls import path

from .views import auth

# NOTE: 不正な会員登録が行われるのを防ぐために、システム管理者が事前に
app_name = "common"
urlpatterns = [
    # path("auth/signup/", auth.signup_view, name="signup"),
    path("auth/login/", auth.login_view, name="login"),
    path("auth/basic/", auth.basic_view, name="basic"),
]
