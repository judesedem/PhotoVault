from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('username','email','id','password')
            
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=120)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','password']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)

        token['name']=user.name
        token['email']=user.email
        token['id']=user.id

        return token