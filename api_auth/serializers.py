from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction

from api_auth.models import Profile


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='profile.organization',
                                         allow_blank=True)
    address = serializers.CharField(
        source='profile.address',
        allow_null=True,
        required=False,
    )
    occupation = serializers.CharField(
        source='profile.occupation',
        allow_null=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'address', 'organization', 'occupation',
                  'email',
                  )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        with transaction.atomic():
            user = super().create(validated_data)
            user.save()
            user.apiuser = self.update_or_create_profile(user, profile_data)
            # send_password_reset(email=validated_data["email"], welcome=True)
            return user
        return None

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        user.profile = self.update_or_create_profile(user, profile_data)
        return user

    def update_or_create_profile(self, user, profile_data):
        profile, created = Profile.objects.update_or_create(
            user=user, defaults=profile_data
        )
        return profile
