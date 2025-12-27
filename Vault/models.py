import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True)

from django.core.serializers.json import DjangoJSONEncoder


# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj,User ):
#             return str(obj)
#         return super().default(obj)
    

class PhotoVault(models.Model):
    user=models.ForeignKey('Vault.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=120)
    description=models.TextField(null=True, blank=True)
    photo=models.ImageField(upload_to="Photos/")
    Public=models.BooleanField(default=True)
    

    def __str__(self):
        return self.title
  

