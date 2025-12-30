from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,MyTokenObtainPairView,LoginView,PhotoView,PhotoDetailView

urlpatterns=[   
    path('token/',TokenObtainPairView.as_view()),
    path('register/',RegisterView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('login/',LoginView.as_view()),
    path('photos/',PhotoView.as_view()),
    path('photos/<int:pk>',PhotoDetailView.as_view())
]