from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=255,unique=True,default="Student")
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255,default=user_name, null=True,blank=True)
    department = models.CharField(max_length=255, default=" ", null=True,blank=True)
    bio       = models.TextField(max_length=500, default=" ", null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
    
    def __str__(self):
        return self.email
