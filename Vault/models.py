import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
class PhotoVault(models.Model):
    user=models.ForeignKey('Vault.User',on_delete=models.CASCADE)
  

