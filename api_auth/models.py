from django.contrib.auth.models import User
from django.db import models
import uuid

MAX_API_CALLS_PER_TOKEN = 10000


class APIUser(User):
    pass


class Token(models.Model):
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(APIUser, null=True)
    api_calls = models.IntegerField(default=0)
    call_limit = models.IntegerField(default=MAX_API_CALLS_PER_TOKEN)
    created_on = models.DateTimeField(editable=False, auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
