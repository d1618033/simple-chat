from django.views.generic import TemplateView, DetailView
from simplechat.models import Room, Participant


class Index(TemplateView):
    template_name = "simplechat/index.html"


class RoomView(DetailView):
    queryset = Room.objects.all()
    template_name = "simplechat/room.html"
