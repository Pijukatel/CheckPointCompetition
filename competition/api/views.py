from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from competition.api import serializers
from competition.models import UserPosition, CheckPoint, Membership

@login_required
@api_view(["GET"])
def user_positions(request):
    serializer = serializers.UserPositionSerializer(UserPosition.objects.all(), many=True)
    return Response(serializer.data)

@login_required
@api_view(["GET"])
def checkpoint_positions(request):
    serializer = serializers.CheckpointPositionSerializer(CheckPoint.objects.all(), many=True)
    return Response(serializer.data)

@login_required
@api_view(["GET"])
def memberships(request):
    serializer = serializers.MembershipSerializer(Membership.objects.all(), many=True)
    return Response(serializer.data)