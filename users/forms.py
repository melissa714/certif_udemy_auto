from django import forms  
from .models import Location,Profile
from localflavor.us.models import USZipCodeField
from django.contrib.auth.models import User
from .widgets import CustomerPictureImageFieldWidget

class UserForm(forms.ModelForm):
    # rend le champs non modifiable
    username = forms.CharField(disabled=True)
    class Meta:
        model=User
        fields =('username','first_name','last_name')

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomerPictureImageFieldWidget)
    bio=forms.TextInput()
    class Meta:
        model=Profile 
        fields=('photo','bio','phone_number')



class LocationForm(forms.ModelForm):
    address_1=forms.CharField(max_length=200,required=True)
    zip_code= USZipCodeField(blank=True)
    
    class Meta:
        model = Location
        fields={'address_1','address_2','city','state','zip_code'}

