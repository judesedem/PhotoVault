# from django.contrib import admin
# from .models import PhotoVault,Album,User

# @admin.register(PhotoVault)
# class PhotoAdmin(admin.ModelAdmin):
#     list_display=('title','photo','is_public','uploaded_at')

#     def get_queryset(self, request):
#         privacy_check=super().get_queryset(request)
#         return privacy_check.filter(is_public=True)
    

# @admin.register(Album)
# class AlbumAdmin(admin.ModelAdmin):
#     list_display=('album')

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=('username','email','is_staff','is_superuser')

from django.contrib import admin
from .models import PhotoVault, Album, User

@admin.register(PhotoVault)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'uploaded_at')
    list_filter = ('is_public', 'user')
    search_fields = ('title', 'user__username')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Superusers see everything
        if request.user.is_superuser:
            return qs
        
        # Regular admins only see public photos
        return qs.filter(is_public=True)
    
    def has_change_permission(self, request, obj=None):
        # Superusers can edit everything
        if request.user.is_superuser:
            return True
        
        # Regular admins can only edit public photos
        if obj is not None and not obj.is_public:
            return False  # Can't edit private photos
        
        return True
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete
        return request.user.is_superuser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')