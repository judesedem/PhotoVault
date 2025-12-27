from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    email=serializers.EmailField()

    class Meta:
        model=User
        fields=('username','email','id','password')

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email exists") 
        return value  
    
    def validate_user(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
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

        token['name']=user.username
        token['email']=user.email
        token['id']=str(user.id)

        return token
    

# from django.core.serializers import serialize

# serialize("json", User.objects.all(), cls=LazyEncoder)