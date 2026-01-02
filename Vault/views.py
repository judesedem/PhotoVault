from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


from .throttle import PhotoRequestThrottle

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import generics
from .models import User,PhotoVault
from .serializers import SignupSerializer,LoginSerializer,PhotoSerializer

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from .serializers import MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view



class RegisterView(CreateAPIView):
    serializer_class=SignupSerializer
    permission_classes=[AllowAny]
    queryset=User.objects.all()


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'message':'Login Successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),


                    
                    'user': {
                        'id': str(user.id),  
                        'email': user.email,
                        'username': user.username
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerorReadOnly
class PhotoView(APIView):
    throttle_classes=[PhotoRequestThrottle]
     
    permission_classes=[IsAuthenticated,IsOwnerorReadOnly]
    def post(self,request):
        serializer=PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request):
        throttle_classes = [UserRateThrottle]
        photos=PhotoVault.objects.filter(user=request.user)
        serializer=PhotoSerializer(photos,many=True)
        return Response(serializer.data)
    
class PhotoDetailView(APIView):
    permission_classes=[IsAuthenticated,IsOwnerorReadOnly]
    throttle_classes=[PhotoRequestThrottle]

    def get_object(self,pk):
        try:
            return PhotoVault.objects.get(pk=pk, user=self.request.user)
        
        except PhotoVault.DoesNotExist:
            return None
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request,pk):
        photo=self.get_object(pk)
        if not photo:
            return Response(
                {'error':'Photo not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=PhotoSerializer(photo)
        return Response(serializer.data)
    
    def put(self,request,pk):
        photo=self.get_object(pk)
        if not photo:
            return Response({
                'error':'Photo Not Found'
            },status=status.HTTP_404_NOT_FOUND)
        serializer=PhotoSerializer(photo,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        photo=self.get_object(pk)
        if not photo:
            return Response(
                {'error':'Photo Not Found'},status=status.HTTP_404_NOT_FOUND
            )
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

          
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

from django.shortcuts import get_list_or_404

class AllPublicPhotosView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerorReadOnly]
    throttle_classes = [PhotoRequestThrottle] 
    
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request):
        photo = get_list_or_404(PhotoVault, is_public=True)
        serializer = PhotoSerializer(photo, many=True)
        return Response(serializer.data)
