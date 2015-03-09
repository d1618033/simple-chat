from rest_framework import serializers
from simplechat.models import Room


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="simplechat:room_detail")

    class Meta:
        model = Room
        fields = ('url',)