import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True)
    

class PhotoVault(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='photos')
    title=models.CharField(max_length=120)
    description=models.TextField(null=True, blank=True)
    photo=models.ImageField(upload_to="Photos/")
    is_public=models.BooleanField(default=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.title
  
#add the album model
