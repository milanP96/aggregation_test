from rest_framework import serializers

from aggregator.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for event model"""

    class Meta:
        model = Event
        fields = ('timestamp', 'domain', 'requests_number',)