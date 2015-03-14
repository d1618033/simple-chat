from rest_framework import serializers
from simplechat.models import Room, Participant, Message


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat_api:room-detail")
    view_url = serializers.HyperlinkedIdentityField(view_name="simplechat:room_detail")
    participant_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ('url', 'view_url', 'participant_set')


class ParticipantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat_api:participant-detail")

    class Meta:
        model = Participant
        fields = ('url', 'pk', 'room', 'name')


class MessageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat_api:message-detail")
    name = serializers.ReadOnlyField(source='participant.name')

    class Meta:
        model = Message
        fields = ('url', 'pk', 'room', 'participant', 'name', 'message')