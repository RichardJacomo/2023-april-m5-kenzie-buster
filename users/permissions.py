from rest_framework import permissions
from users.models import User
from django.shortcuts import get_object_or_404


class IsAdminOrNot(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.method == 'PATCH' or request.method == 'GET':
            user_id = view.kwargs.get('user_id')
            user = get_object_or_404(User, pk=user_id)

            if user == request.user:
                return True
        
        return False