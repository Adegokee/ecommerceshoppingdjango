from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not username:
            raise ValueError('Please provide a username')
        if not email:
            raise ValueError('Please provide a email address')
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, username, email, password):
        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name, 
            last_name=last_name, 
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    
class Account(AbstractBaseUser):
    username=models.CharField(max_length=100, unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['first_name', 'last_name', 'username']
    objects= MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    
