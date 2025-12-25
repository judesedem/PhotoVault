from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,MyTokenObtainPairView

urlpatterns=[
    #Auth endpoints
    path('token/',TokenObtainPairView.as_view()),
    path('register/',RegisterView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('login/',MyTokenObtainPairView.as_view())
]