from django.db import models
from .consts import CAR_BRANDS,TRANSMISSION_OPTIONS
import uuid
from users.models import Profile,Location
from .utils import user_listing_path
from django.utils.html import mark_safe

# Create your models here.

class Listing(models.Model):
    """creation de table listing"""
    id= models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller= models.ForeignKey(Profile,on_delete=models.CASCADE)
    brand= models.CharField(max_length=100,choices=CAR_BRANDS,default=None,verbose_name="Marque")
    model=models.CharField(max_length=100,verbose_name="modele")
    vin=models.CharField(max_length=50)
    mileage=models.IntegerField(default=0,verbose_name="kilométrage")
    color= models.CharField(max_length=50,null=True)
    description=models.TextField(null=True)
    engine = models.CharField(max_length = 150,null=True)
    transmission= models.CharField(max_length=150,choices=TRANSMISSION_OPTIONS,default=None)
    location=models.OneToOneField(Location,on_delete=models.SET_NULL,null=True)
    image=models.ImageField(upload_to=user_listing_path,null=True)
    
    @property
    def image_view(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" />'.format(self.image.url))
        return ""
    
    class Meta:
        verbose_name_plural = " Vehicules Enregistrée(s)"

    def __str__(self) -> str:
        return f'{self.seller.user.username}\'s Listing -{self.model}'
    
    

class LikedListing(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    like_date=models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Voiture Likée"
    def __str__(self):
        return f'{self.listing.model} lsiting liked by {self.profile.user.username}'