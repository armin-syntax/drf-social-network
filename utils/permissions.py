from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_related_user(obj, user, fields=['user', 'owner', 'author']):
    if obj == user:
        return True
    
    for field in fields:
        related_user = getattr(obj, field, None)
        if related_user == user:
            return True
    
    return False


class IsAnonymousPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return is_related_user(obj, request.user)


class IsOwnerOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return is_related_user(obj, request.user)


class IsNotSelfPermission(BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username')
        return request.user.username != username
