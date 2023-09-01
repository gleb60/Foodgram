from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdminOrSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return request.user.is_authenticated and request.user.is_admin
