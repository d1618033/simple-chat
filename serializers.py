from rest_framework import serializers
from simplechat.models import Room, Participant


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat:room_detail")

    class Meta:
        model = Room
        fields = ('url',)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('room', 'name')