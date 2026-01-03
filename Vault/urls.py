from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,LoginView,PhotoView,PhotoDetailView,AllPublicPhotosView,AllPrivatePhotosView,LogoutView
from .import views
urlpatterns=[   
    path('token/',TokenObtainPairView.as_view()),
    path('signup/',RegisterView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('photo/',PhotoView.as_view()),
    path('photo/<int:pk>/',PhotoDetailView.as_view()),
    path('all_public_photos/',AllPublicPhotosView.as_view()),
    path('all_private_photos',AllPrivatePhotosView.as_view())
]