from rest_framework import permissions
from django.shortcuts import get_object_or_404

from simplechat.models import Participant


class SafeMethodsOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class CanEditParticipant(SafeMethodsOnly):
    def has_object_permission(self, request, view, obj=None):
        if obj is None:
            can_edit = True
        else:
            if obj.password != request.data.get('password', ''):
                can_edit = False
            else:
                can_edit = True
        result = can_edit or super(CanEditParticipant, self).has_object_permission(request, view, obj)
        return result


class CanEditMessage(SafeMethodsOnly):
    def has_object_permission(self, request, view, obj=None):
        participant_pk = request.data['participant']
        participant = get_object_or_404(Participant, pk=participant_pk)
        if participant.password == request.data.get('password', ''):
            return True
        else:
            return super(CanEditMessage, self).has_object_permission(request, view, obj)