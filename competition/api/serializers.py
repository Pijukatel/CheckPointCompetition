from rest_framework import serializers
from competition.models import UserPosition, CheckPoint, Membership, Point, Team
from django.contrib.auth.models import User

class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        read_only_fields = ('user',)
        fields = ("gps_lat", "gps_lon", "user")


class CheckpointPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPoint
        fields = ("gps_lat", "gps_lon", "name")


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ("confirmed", "checkpoint_id", "team_id")


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name", "confirmed")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
