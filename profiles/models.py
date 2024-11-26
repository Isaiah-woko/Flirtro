from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _


# Manager for User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


# User model
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    display_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    heading = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # To make users staff/admin

    # Relationships
    roles = models.ManyToManyField('Role', related_name='users', blank=True)

    # Custom manager for user creation
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = self.set_password(password)

    def check_password(self, password):
        return self.check_password(password)

    def activate(self):
        self.is_active = True

    @property
    def actived_subscription(self):
        return self.is_active


# Role model
class Role(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
