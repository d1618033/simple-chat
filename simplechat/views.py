from django.views.generic import FormView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from simplechat.models import Room, Participant
from simplechat.forms import NewRoomForm, RegisterForm


class Index(FormView):
    template_name = 'simplechat/index.html'
    form_class = NewRoomForm

    def form_valid(self, form):
        room_id = form.create()
        return HttpResponseRedirect(reverse("simplechat:room_register", args=(room_id, )))


class RoomRegister(FormView):
    template_name = 'simplechat/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        room_pk = self.kwargs['pk']
        name = form.create(room_pk)
        self.request.session['name'] = name
        return HttpResponseRedirect(reverse("simplechat:room_detail", args=(room_pk,)), )


class RoomView(DetailView):
    queryset = Room.objects.all()
    template_name = "simplechat/room.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        if 'name' in self.request.session:
            context['name'] = self.request.session['name']
            del self.request.session['name']
        return context