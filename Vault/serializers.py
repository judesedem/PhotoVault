from rest_framework import serializers
from .models import User,PhotoVault,Album
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignupSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    email=serializers.EmailField()

    class Meta:
        model=User 
        fields=('username','email','id','password')

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exists!') 
        return value  
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exists')
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

class PhotoSerializer(serializers.ModelSerializer):
    uploaded_at=serializers.DateTimeField(read_only=True)
    user=serializers.ReadOnlyField(source='user.username')
    album=serializers.CharField(write_only=True)
    # album_name=serializers.CharField(source=)
    
    

    class Meta:
        model=PhotoVault
        fields=('title','photo','description','album','user','uploaded_at','is_public','id') 

    def create(self, validated_data): 
        album= validated_data.pop('album')
        album, _ = Album.objects.get_or_create(album=album) 
        photo = PhotoVault.objects.create(album=album, **validated_data) 
        return photo      
       
class AlbumSerializer(serializers.ModelSerializer):
    album_name=serializers.CharField()
    class Meta:
        Model=Album
        fields='__all__'