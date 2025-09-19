from rest_framework import serializers

from .models import Ride, Ride_Event, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer()
    id_driver = UserSerializer()

    class Meta:
        model = Ride
        fields = "__all__"


class Ride_EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride_Event
        fields = "__all__"
