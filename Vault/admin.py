from django.contrib import admin
from .models import PhotoVault

@admin.register(PhotoVault)
class PhotoAdmin(admin.ModelAdmin):
    display=('photo','title','uploaded_at')
    def get_queryset(self, request):
        privacy_check=super().get_queryset(request)
        return privacy_check.filter(is_public=True)
    
class ViewUsers(admin.ModelAdmin):
    display=('username','email','id','is_staff','is_superuser')


