
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import generics
from .models import User
from .serializers import UserSerializer,LoginSerializer

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from .serializers import MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[AllowAny]
    queryset=User.objects.all()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


    
# class UserListView(generics.ListAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSerializer

# class CustomLogin(generics.GenericAPIView):
#     serializer_class=LoginSerializer

#     def post(self,request,*args,**kwargs):
#         username=request.data.get("username")
#         password=request.data.get("password")
#         user=authenticate(username=username, password=password)
#         if user is not None:
#             refresh=RefreshToken.for_user(user)
#             serializer=UserSerializer(user)
#             return Response(
#                 {
#                     "Refresh":str(refresh),
#                     "Access":str(refresh.access_token),
#                     "user":serializer.data
#                 }
#             )
#         else:
#             return Response(
#                 {
#                     "Error":"UserNotFound"
#                 }
#             )