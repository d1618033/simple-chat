from django.views.generic import TemplateView, DetailView
from simplechat.models import Room
from rest_framework.generics import ListCreateAPIView
from simplechat.serializers import RoomSerializer


class Index(TemplateView):
    template_name = "simplechat/index.html"


class RoomList(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomView(DetailView):
    queryset = Room.objects.all()
    template_name = "simplechat/room.html"


