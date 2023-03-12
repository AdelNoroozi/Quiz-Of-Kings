from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegisterView, UserView, ChangePasswordView, UserInfoView, UserUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user_view'),
    path('user/info/', UserInfoView.as_view(), name='user_info'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('user/update-profile/', UserUpdateView.as_view(), name='change_password'),
]
