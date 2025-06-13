from django.urls import path
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserListView,
    UserDetailView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    AccountDeleteConfirmView, 
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'), # Admin only
    path('users/me/', UserDetailView.as_view(), {'pk': 'me'}, name='user-me-detail'), 
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'), 
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('confirm-delete-account/<str:uidb64>/<str:token>/', AccountDeleteConfirmView.as_view(), name='confirm-delete-account'), 
]