from django.contrib import admin

from api_auth.models import Profile, Token


admin.site.register(Profile)
admin.site.register(Token)
