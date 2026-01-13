from rest_framework_role_filters.role_filters import RoleFilter
from .serializers import UserSerializer
from rest_framework.permissions import SAFE_METHODS


class AdminRoleFilter(RoleFilter):
    role_id = 'admin'


class UserRoleFilter(RoleFilter):
    role_id = 'user'
    
    def get_allowed_actions(self, request, view, obj=None):
        # This example returns same list both for "global permissions" check,
        # and for "object" permissions, but different list may be returned
        # if `obj` argument is not None, and this list will be used to check
        # if action is allowed during call to `ViewSet.check_object_permissions`
        if request.method in SAFE_METHODS:
            return ['list', 'retrieve']
        return ['create', 'list', 'retrieve', 'update', 'partial_update']
    
    def get_queryset(self, request, view, queryset):
        queryset = queryset.filter(user=request.user)
        return queryset
    
    def get_serializer_class(self, request, view):
        return UserSerializer
    
    def get_serializer(self, request, view, serializer_class, *args, **kwargs):
        fields = ('role', 'username', 'created_at')
        return serializer_class(*args, fields=fields, **kwargs)