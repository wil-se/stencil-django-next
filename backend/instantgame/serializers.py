from rest_framework import serializers
from .models import InstantGame, InstantGameSettings, CoinFlip
from randomhandler.serializers import ExtractedNumberSerializer
from authentication.serializers import UserSerializer


class InstantGameSerializer(serializers.ModelSerializer):
    extracted_number = ExtractedNumberSerializer()
    player = UserSerializer()
    settings = InstantGameSettings()

    class Meta:
        model = InstantGame
        fields = "__all__"


class CoinFlipSerializer(serializers.ModelSerializer):
    extracted_number = ExtractedNumberSerializer()
    player = UserSerializer()

    class Meta:
        model = CoinFlip
        fields = "__all__"


class InstantGameSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstantGameSettings
        fields = "__all__"