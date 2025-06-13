from django.shortcuts import render, get_object_or_404 # Added get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail # Import send_mail
from django.conf import settings 
from django.urls import reverse 

# Placeholder for frontend URL, configure this in your settings.py
FRONTEND_PASSWORD_RESET_CONFIRM_URL = getattr(settings, 'FRONTEND_PASSWORD_RESET_CONFIRM_URL', 'http://localhost:3000/auth/reset-password-confirm/') # Example frontend URL
ACCOUNT_DELETION_CONFIRM_PATH_NAME = 'confirm-delete-account' # for reverse()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer 
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['user'] = UserSerializer(self.user).data
        return response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.kwargs.get(self.lookup_field) == 'me':
            return self.request.user
        # For admin accessing specific user by ID
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_to_delete = instance 

        if not (request.user == user_to_delete or request.user.is_superuser):
            return Response({"detail": "You do not have permission to delete this account."},
                            status=status.HTTP_403_FORBIDDEN)

        token = default_token_generator.make_token(user_to_delete)
        uid = urlsafe_base64_encode(force_bytes(user_to_delete.pk))
        
        confirm_path = reverse(ACCOUNT_DELETION_CONFIRM_PATH_NAME, kwargs={'uidb64': uid, 'token': token})
        
        api_base_url = getattr(settings, 'API_BASE_URL', request.scheme + "://" + request.get_host())
        confirmation_url = f"{api_base_url}{confirm_path}"

        subject = 'Confirm Account Deletion for Waba Yangu'
        message = (
            f"Hello {user_to_delete.name},\n\n"
            f"We received a request to delete your account on Waba Yangu.\n"
            f"To confirm this action and permanently delete your account, please click the link below:\n"
            f"{confirmation_url}\n\n"
            f"If you did not request this, please ignore this email. Your account will not be deleted.\n\n"
            f"This link is valid for a limited time.\n\n"
            f"Thanks,\nThe Waba Yangu Team"
        )
        try:
            send_mail(
                subject,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                [user_to_delete.email],
                fail_silently=False,
            )
            return Response(
                {"detail": "A confirmation email has been sent to delete your account. Please check your inbox."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Log the exception e (e.g., import logging; logging.error(f"Email sending failed: {e}"))
            return Response(
                {"detail": "There was an error sending the confirmation email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AccountDeleteConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, DjangoUnicodeDecodeError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.delete() # Or user.is_active = False; user.save() for soft delete
            return Response({"detail": "Account successfully deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Deletion link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal if the user exists or not for security reasons
            return Response({"detail": "If an account with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_link_frontend = f"{FRONTEND_PASSWORD_RESET_CONFIRM_URL}{uid}/{token}/"
        
        subject = 'Password Reset Request for Waba Yangu'
        message = (
            f"Hello {user.name},\n\n"
            f"You requested a password reset for your Waba Yangu account.\n"
            f"Please click the link below to set a new password:\n"
            f"{reset_link_frontend}\n\n"
            f"If you did not request a password reset, please ignore this email.\n\n"
            f"This link is valid for a limited time.\n\n"
            f"Thanks,\nThe Waba Yangu Team"
        )
        
        try:
            send_mail(
                subject,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                [email],
                fail_silently=False,
            )
            return Response({"detail": "If an account with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception e
            return Response({"detail": "There was an error sending the password reset email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
