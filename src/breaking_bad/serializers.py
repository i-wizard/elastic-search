from rest_framework import serializers

from breaking_bad.models import Character, Location


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = "__all__"
        read_only_fields = ("is_deleted", "deleted_at")


class CreateLocationSerializer(serializers.Serializer):
    longitude = serializers.DecimalField(max_digits=9, decimal_places=7)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    character_id = serializers.CharField(max_length=255)


class LocationSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    distance = serializers.FloatField(required=False)

    class Meta:
        model = Location
        fields = "__all__"
