from simplechat.models import Room, Participant
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from simplechat_api.serializers import RoomSerializer, ParticipantSerializer


class RoomList(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ParticipantList(ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ParticipantDetail(RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer