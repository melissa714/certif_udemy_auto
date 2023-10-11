from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField,USZipCodeField
from django.utils.html import mark_safe

from .utils import user_directory_path
# Create your models here.

class Location(models.Model):
    address_1 = models.CharField(max_length = 150,blank=True)
    address_2 = models.CharField(max_length = 150,blank=True)
    city = models.CharField(max_length = 150,blank=True)
    state=USStateField(default='NY')
    zip_code=USZipCodeField(blank=True)

    
    def __str__(self):
        return f'le pays est {self.state}'
   
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(null=True,upload_to=user_directory_path,blank=True)
    bio=models.CharField(max_length=140,blank=True)
    phone_number= models.CharField(max_length=12,blank=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL,null=True)
    
    @property
    def Photo(self):
        if self.photo:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.photo.url))
        return ""
    

    
    def __str__(self) -> str:
        return f'Profile {self.user.username}'