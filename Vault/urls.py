from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,LoginView,PhotoView,PhotoDetailView
from .import views
urlpatterns=[   
    path('token/',TokenObtainPairView.as_view()),
    path('register/',RegisterView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('login/',LoginView.as_view()),
    path('photos/',PhotoView.as_view()),
    path('photos/<int:pk>',PhotoDetailView.as_view()),
    path('all_public_photos/',views.all_public_photos)
]