from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, owner_name, state, school_name, phone_number, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            owner_name=owner_name,
            state=state,
            school_name=school_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    owner_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    school_name = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'owner_name', 'state', 'school_name', 'phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
