from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', views.register_user, name='register'),
    path('get-user/', views.get_user, name='get-user'),
    path('update-user/', views.update_user, name='update-user'),
    path('delete-user/', views.delete_user, name='delete-user'),
]