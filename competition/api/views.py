from django.contrib.auth.decorators import login_required
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from competition.api.serializers import UserPositionSerializer, CheckpointPositionSerializer, MembershipSerializer
from competition.models import UserPosition, CheckPoint, Membership


@login_required
@api_view(["GET", "PATCH"])
def user_positions(request):
    if request.method == "GET":
        serializer = UserPositionSerializer(UserPosition.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == "PATCH":
        current_position = UserPosition.objects.get(user=request.user)
        serializer = UserPositionSerializer(instance=current_position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(["GET"])
def checkpoint_positions(request):
    serializer = CheckpointPositionSerializer(CheckPoint.objects.all(), many=True)
    return Response(serializer.data)


@login_required
@api_view(["GET"])
def memberships(request):
    serializer = MembershipSerializer(Membership.objects.all(), many=True)
    return Response(serializer.data)
