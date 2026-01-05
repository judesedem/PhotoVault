from rest_framework.permissions import BasePermission,SAFE_METHODS
#Private photos should only be accessible to their owners
# , while public photos can be viewed by others and may be
#  deleted by the owner or an admin if deemed inappropriate,
#private photos can only be viewed by admin but not changed

class IsOwnerorReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):        
        if request.method in SAFE_METHODS:
            if obj.is_public:
                return True            
            return obj.user==request.user and request.user.is_staff
        return obj.user==request.user 
    
    
             