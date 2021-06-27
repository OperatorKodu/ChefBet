from rest_framework import serializers
from .models import Event

class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'host', 'guest', 'types', 'datetime']
