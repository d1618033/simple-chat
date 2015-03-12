from rest_framework import serializers
from simplechat.models import Room, Participant


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat_api:room_detail")
    view_url = serializers.HyperlinkedIdentityField(view_name="simplechat:room_detail")
    participant_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ('url', 'view_url', 'participant_set')


class ParticipantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat_api:participant_detail")

    class Meta:
        model = Participant
        fields = ('url', 'room', 'name')