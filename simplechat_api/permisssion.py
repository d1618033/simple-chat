from rest_framework import permissions


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
