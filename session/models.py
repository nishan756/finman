from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from django.utils.timezone import now
from django_summernote.fields import SummernoteTextField
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email = email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active = True')
        
        return self.create_user(email = email , password = password , **extra_fields)
    
class CustomUser(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 11 , blank = True,null = True)
    username = models.CharField(max_length = 50,blank = True,null = True)
    club_name = models.CharField(max_length = 100)
    club_logo = models.ImageField(blank = True,null = True , upload_to = 'club_logo')
    established_at = models.DateField(blank = True,null = True)
    details = SummernoteTextField(blank = True)

    # Superuser credentials
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(default = now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.username 
    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'




