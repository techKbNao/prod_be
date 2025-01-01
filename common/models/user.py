import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class TKBUser(AbstractUser):
    """
    Tech Knowledge Base の提供するベースユーザー
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firebase_uid = models.CharField(default="", max_length=28)
    # REVIEW: on_deleteは一旦
    # REVIEW: null = Falseにする
    # REVIEW createsuperuserコマンドをカスタマイズ

    def __str__(self):
        return self.username
