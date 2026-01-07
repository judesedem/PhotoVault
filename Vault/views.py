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
from rest_framework_simplejwt import authentication

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import generics
from .models import User,PhotoVault
from .serializers import SignupSerializer,LoginSerializer,PhotoSerializer,UserSerializer

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from .serializers import MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView


from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated,IsAdminUser



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
                        'username': user.username,
                        'role':user.role
                        
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
         try:
             refresh_token=request.data.get("refresh")

             if not refresh_token:
                 return Response({
                     "error":"Refresh token is required"
                 }, status=status.HTTP_400_BAD_REQUEST)
             
             token=RefreshToken(refresh_token)
             token.blacklist()
             return Response({
                 "message":"Successfully logged out"
             },status=status.HTTP_205_RESET_CONTENT)
         
         except TokenError as e:
             return Response(
                 {
                     "error":"Invalid or expired token"
                 },
                 status=status.HTTP_400_BAD_REQUEST
             )
         except Exception as e:
             return Response(
                 {"error":"Something went wrong"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
             )
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerorReadOnly
class PhotoView(APIView):     
    permission_classes=[IsAuthenticated,IsOwnerorReadOnly]
    def post(self,request):
        serializer=PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request):
        photos=PhotoVault.objects.filter(user=request.user)
        serializer=PhotoSerializer(photos,many=True)
        return Response(serializer.data)
    
class PhotoDetailView(APIView):
    permission_classes=[IsOwnerorReadOnly]
    throttle_scope='photo'

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
        return Response({'message':'Successfully Deleted'},status=status.HTTP_204_NO_CONTENT)

       
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class AllPublicPhotosView(APIView):
    permission_classes = [IsAuthenticated]   
    throttle_scope='photo'
    
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request):
        photo=PhotoVault.objects.filter(is_public=True)
        if not photo.exists():
            return Response({'detail':'No public photos available'},status=status.HTTP_404_NOT_FOUND)
        serializer=PhotoSerializer(photo,many=True)
        return Response(serializer.data)
            
#JUDE1
#judesedem@gmail.com
#admin1
class MyPublicPhotosView(APIView):
    permission_classes = [IsAuthenticated]   
    throttle_scope='photo'
    
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request):
        photo=PhotoVault.objects.filter(is_public=True,user=request.user)
        if not photo.exists():
            return Response({'detail':'You have no public photos'},status=status.HTTP_404_NOT_FOUND)
        serializer=PhotoSerializer(photo,many=True)
        return Response(serializer.data)
    
class AllPrivatePhotosView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = 'photo'
    
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request):
        
        photos = PhotoVault.objects.filter(
            is_public=False,
            user=request.user
        )
        
        
        if not photos.exists():
            return Response(
                {"detail": "You have no private photos."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)
class AllUsersView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializer(user,many=True)
        return Response(serializer.data)
    