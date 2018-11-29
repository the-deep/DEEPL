from rest_framework import serializers

from .models import Country


class CountryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'iso2', 'iso3')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country


class FuzzyCountrySerializer(CountryShortSerializer):
    similarity = serializers.FloatField(read_only=True)

    class Meta:
        model = CountryShortSerializer.Meta.model
        fields = CountryShortSerializer.Meta.fields + ('similarity',)
