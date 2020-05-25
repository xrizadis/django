from rest_framework import serializers
from core.models import Tag, Component


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag objects"""

    class Meta():
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class ComponentSerializer(serializers.ModelSerializer):
    """seriazer for compoentn objects"""
    class Meta():
        model = Component
        fields = ("id", "name")
        read_only_fields = ("id",)
