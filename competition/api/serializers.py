from rest_framework import serializers
from competition.models import UserPosition, CheckPoint, Membership


class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        read_only_fields = ('user',)
        fields = ("gps_lat", "gps_lon", "user")


class CheckpointPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPoint
        fields = ("gps_lat", "gps_lon", "name")


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"
