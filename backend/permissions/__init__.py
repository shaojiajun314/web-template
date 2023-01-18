from rest_framework.permissions import BasePermission


class IsLogin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and \
            super().has_permission(request, view)


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and \
            request.user.is_staff and super().has_permission(request, view)


class HasMobile(IsLogin):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.mobile
