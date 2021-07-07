from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Event, Coupon, Wallet


class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'host', 'guest', 'types', 'start_datetime']
        read_only_fields = ['id', 'host', 'guest', 'types', 'start_datetime']


class CouponsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'types', 'odds', 'contribution', 'prize', 'author']
        read_only_fields = ['id', 'odds', 'prize', 'author']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ['owner', 'money']
        read_only_fields = ['owner']

