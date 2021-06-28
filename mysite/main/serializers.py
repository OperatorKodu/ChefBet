from rest_framework import serializers
from .models import Event, Coupon
from django.contrib.auth.models import User


class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'host', 'guest', 'types', 'datetime']

class CouponsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['types', 'odds', 'contribution', 'prize', 'author']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']