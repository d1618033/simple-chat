from django.views.generic import TemplateView, DetailView
from simplechat.models import Room, Participant
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from simplechat.serializers import RoomSerializer, ParticipantSerializer


class Index(TemplateView):
    template_name = "simplechat/index.html"


class RoomList(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomView(DetailView):
    queryset = Room.objects.all()
    template_name = "simplechat/room.html"


class ParticipantList(ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ParticipantDetail(RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer