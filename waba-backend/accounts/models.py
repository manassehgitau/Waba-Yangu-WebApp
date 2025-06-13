import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from cloudinary.models import CloudinaryField

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    """
    Custom user model for the application.
    """
    SUBSCRIPTION_TYPE_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Remove username, first_name, and last_name fields from AbstractBaseUser
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    profile_picture = CloudinaryField(
        'profile_picture',  
        folder='profile_pics', 
        null=True, blank=True)
    subscription_type = models.CharField(max_length=50, default="free")
    is_subscription_active = models.BooleanField(default=True)
    subscription_expires = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser