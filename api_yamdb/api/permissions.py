from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    message = 'У вас недостаточно прав для совершения действия'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser
                or request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_authenticated
                and request.user.role == 'moderator'
                )


class IsAdministratorRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser
        )
