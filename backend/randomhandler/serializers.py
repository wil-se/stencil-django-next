from rest_framework import serializers
from .models import HashChainIndex, ExtractedNumber


class HashChainIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashChainIndex
        fields = "__all__"


class ExtractedNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedNumber
        fields = "__all__"