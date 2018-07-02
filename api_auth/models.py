from django.contrib.auth.models import User
from django.db import models
import uuid
import random

MAX_API_CALLS_PER_TOKEN = 10000
KEY_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_verification_key():
    """Generate 8 char long keys"""
    return ''.join([random.choice(KEY_CHARS) for _ in range(8)])


class Profile(models.Model):
    user = models.OneToOneField(User)
    verified = models.BooleanField(default=False)
    verification_key = models.CharField(
        max_length=15, default=generate_verification_key
    )
    address = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id or not self.tokens:
            # save and then generate a token
            super().save(*args, **kwargs)
            Token.objects.create(user=self)
        else:
            super().save(*args, **kwargs)

    @property
    def test_token(self):
        tokens = self.tokens.filter(is_test=True)
        if not tokens:
            return None
        return str(tokens[0])

    @property
    def api_token(self):
        tokens = self.tokens.filter(is_test=False)
        if not tokens:
            return None
        return str(tokens[0])


class Token(models.Model):
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile, null=True, related_name='tokens')
    is_test = models.BooleanField(default=True)
    api_calls = models.IntegerField(default=0)
    call_limit = models.IntegerField(default=MAX_API_CALLS_PER_TOKEN)
    created_on = models.DateTimeField(editable=False, auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token[:10]+'...'
