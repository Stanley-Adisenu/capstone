from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.humanize.templatetags.humanize import naturaltime


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=255,unique=True,default="Student" )
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255,default=" ", null=True,blank=True)
    department = models.CharField(max_length=255, default=" ", null=True,blank=True)
    bio       = models.TextField(max_length=500, default=" ", null=True,blank=True)
    avatar = models.ImageField(upload_to = 'dashboard/images/', blank = True, null = True)
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


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    host = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField( auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(UserAccount, related_name='participants', blank=True)

    class Meta:
        ordering = ['-updated','-created']

    @property
    def time_since_created(self):
        # Return human-readable time since the room was created
        return naturaltime(self.created)

    @property
    def participant_count(self):
        # Return the number of participants in the room
        return self.participants.count()

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def time_since_updated(self):
        # Return human-readable time since the message was updated
        return naturaltime(self.updated)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[0:50]
    

