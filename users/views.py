from django.shortcuts import render,redirect
from  django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .forms import UserForm,ProfileForm,LocationForm
# Create your views here.
from main.models import Listing ,LikedListing





def login_view(request):
    if request.method == 'POST':
        login_form=AuthenticationForm(request ,data=request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            print(user)
            if user is not None:
                login(request,user) 
                messages.success(request,f"Tu es maintenant connectée {username}")
                return redirect('home')
            else:
                messages.error(request,f"Désole vos identifiants sont erronés ")         
        else:
                messages.error(request,f"Désole vos identifiants sont erronés ")
    elif request.method == 'GET':
        login_form=AuthenticationForm()
    return render(request,'users/login.html',{'login_form':login_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


class RegisterView(View):
    
    def get(self, request):
        register_form=UserCreationForm()
        return render(request,'users/register.html',{'register_form':register_form})

    def post(self,request):
        register_form=  UserCreationForm(request.POST)
        if register_form.is_valid():
            user=register_form.save()
            user.refresh_from_db()
            # password=register_form.cleaned_data.get('password')
            # user= authenticate(username=user.username,password=password)
            login(request,user)
            messages.success(request,f'félicitations {user.username} vous etes connectée et enregistrée avec succes')
            return redirect('home')
        else:
            messages.error(request,f"Désole vos identifiants sont erronés ")  
            return render(request,'users/register.html',{'register_form':register_form})
 
              
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        user_listing=Listing.objects.filter(seller=request.user.profile)
        user_liked_listings= LikedListing.objects.filter(profile=request.user.profile).all()
        user_form=UserForm(instance=request.user)
        profile_form =ProfileForm(instance=request.user.profile)
        location_form=LocationForm(instance=request.user.profile.location)
        return render(request,'views/profile.html',{'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'location_form':location_form,
                                                    'user_listing':user_listing,
                                                    'user_liked_listings':user_liked_listings,})
    def post(self,request):
        user_form=UserForm(request.POST, instance=request.user)
        profile_form =ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        location_form=LocationForm(request.POST,request.FILES, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request,'Profil est modifié avec succes!')
        else:
            messages.error(request,"erreur lors de la modification du profil")
        return render(request,'views/profile.html',{'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'location_form':location_form,
                                                     })
    
