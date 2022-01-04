from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise TypeError("User's must have an email")
        if not username:
            raise TypeError("User's must have an username")
        if not password:
            raise TypeError("User's must have an password")
        user = self.model(email=self.normalize_email(
            email), username=username)
        user.set_password(password)
        user.save()
        return user

    def edit_user(self, user, email=None, username=None, password=None):
        print(user)
        user.email = email
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_validated = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email


class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now=True)
    written_by = models.CharField(max_length=100)
    writter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_writter_obj(self):
        return self.writter
