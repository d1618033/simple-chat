from rest_framework import viewsets

from simplechat.models import Room, Participant
from simplechat_api.serializers import RoomSerializer, ParticipantSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
