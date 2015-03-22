from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from simplechat.models import Room, Participant, Message
from simplechat_api.serializers import RoomSerializer, ParticipantSerializer, MessageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def check_password(self, request):
        participant_pk = request.data['participant']
        participant = get_object_or_404(Participant, pk=participant_pk)
        if participant.password != request.data.get('password', ''):
            return False
        return True

    def create(self, request, *args, **kwargs):
        if not self.check_password(request):
            raise PermissionDenied
        return super(MessageViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.check_password(request):
            raise PermissionDenied
        return super(MessageViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self.check_password(request):
            raise PermissionDenied
        return super(MessageViewSet, self).partial_update(request, *args, **kwargs)

    @list_route()
    def recent(self, request):
        queryset = self.queryset
        from_pk = request.QUERY_PARAMS.get('from_pk', None)
        room_pk = request.QUERY_PARAMS.get('room_pk', None)
        not_from_participant_pk = request.QUERY_PARAMS.get('not_from_participant_pk', None)
        if room_pk is not None:
            queryset = queryset.filter(room__pk=room_pk)
        if from_pk is not None:
            queryset = queryset.filter(pk__gt=from_pk)
        if not_from_participant_pk is not None:
            queryset = queryset.filter(~Q(participant__pk=not_from_participant_pk))
        return Response(self.serializer_class(queryset, many=True, context={'request': request}).data)