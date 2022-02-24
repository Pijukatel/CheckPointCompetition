from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from competition.api.serializers import UserPositionSerializer, CheckpointPositionSerializer, MembershipSerializer, \
    PointSerializer, TeamSerializer, UserSerializer
from competition.models import UserPosition, CheckPoint, Membership, Point, Team


@login_required
@api_view(["PATCH"])
def current_user_pos(request):
    if request.method == "PATCH":
        current_position = UserPosition.objects.get(user=request.user)
        serializer = UserPositionSerializer(instance=current_position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_positions(request):
    serializer = UserPositionSerializer(UserPosition.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def checkpoint_positions(request):
    serializer = CheckpointPositionSerializer(CheckPoint.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def memberships(request):
    serializer = MembershipSerializer(Membership.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def points(request):
    serializer = PointSerializer(Point.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def teams(request):
    serializer = TeamSerializer(Team.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
