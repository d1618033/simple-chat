from django import forms
from simplechat.models import Participant, Room


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)

    def create(self, room_pk):
        name = self.cleaned_data['name']
        room = Room.objects.get(pk=room_pk)
        participant = Participant(name=name, room=room)
        participant.save()
        return name


class NewRoomForm(forms.Form):
    def create(self):
        room = Room()
        room.save()
        return room.pk