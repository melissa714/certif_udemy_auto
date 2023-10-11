from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Listing,LikedListing
from .forms import ListingForm 
from users.forms import LocationForm
from django.contrib import messages
from .filters import ListingFilter
from imp import reload
from django.core.mail import send_mail
# Create your views here.
from django.core.paginator import Paginator



def page_not_found_view(request,exception):
     return render(request,'views/404.html')


def main_view(request):
    return render(request,"views/main.html",{'name':"meliiissaaa"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    paginator = Paginator(listings, 2)
    listing_filter=ListingFilter(request.GET,queryset=listings)
    user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listings_ids= [l[0] for l in user_liked_listings ]
    context={
        # 'listings':listings,
        'listing_filter':listing_filter,
        'liked_listings_ids':liked_listings_ids
    }
    return render(request,"views/home.html",context)



login_required
# deux formulaires en meme temps
def list_view(request):
    if request.method == 'POST':
        try:
             listing_form=ListingForm(request.POST,request.FILES)
             location_form=LocationForm(request.POST)
             if listing_form.is_valid() and location_form.is_valid():
                 listing=listing_form.save(commit=False)
                 listing_location = location_form.save()
                 listing.seller=request.user.profile 
                 listing.location=listing_location
                 listing.save()
                 messages.info(request,f'{listing.model} Listing Posted Successfully!')
                 return redirect('home')
             else:
                 raise Exception()
        except  Exception as e:
            print(e)
            messages.error(request,"test")
    elif request.method == 'GET':
        listing_form=ListingForm()
        location_form=LocationForm()
    return render(request,"views/list.html",{'listing_form':listing_form,'location_form':location_form})


@login_required
def listing_view(request,id):
    try :
        listing=Listing.objects.get(id=id)
        if listing is None:
            raise Exception 
        return render(request,'views/listing.html',{'listing':listing, })
    except Exception as e:
        messages.error(request,f'invalid {id}')
        return redirect('home')
    
@login_required
def edit_view(request,id):
    try:
        listing=Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form= ListingForm(request.POST,request.FILES,instance=listing) 
            location_form=LocationForm(request.POST,request.FILES,instance=listing.location) 
            print(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(request,f'Listing {id} updated successfull')

                return redirect('home')
            else:
               messages.error(request,f"erreur")
               return reload()
        else:
            listing_form= ListingForm(instance=listing) 
            location_form=LocationForm(instance=listing.location)
        context={
            'location_form':location_form,
            'listing_form':listing_form
        }
    except Exception as e: 
        messages.error(request,f"erreur")
    print(id)
    return render(request,'views/edit.html',context)



@login_required
def like_listing_view(request,id):
    #récupère l'objet d'annonce avec l'ID donné. 
    # Si l'annonce n'existe pas,
    # une erreur 404 est renvoyée
    listing=get_object_or_404(Listing,id=id)
    liked_listing,created=LikedListing.objects.get_or_create(profile=request.user.profile,listing=listing)
    #Si la variable created est False,
    # cela signifie que l'utilisateur a déjà aimé l'annonce. 
    # Dans ce cas, l'objet LikedListing est supprimé.
    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()
    return JsonResponse({
        'is_liked_by_user':created,
    })
    


@login_required
def inquire_listing_using_email(request,id):
    listing = get_object_or_404(Listing,id=id)
    try:
        emailSubject=f'{request.user.username} is interested in {listing.model}'
        emailMessage=f'Salut {listing.seller.user.username},{request.user.username} est interessé(e) par le modele {listing.model} dans liste de voiture'
        send_mail(emailSubject,emailMessage, 'nguessanmelissa01@gmail.com',[listing.seller.user.email,],fail_silently=True)
        return JsonResponse(
            {
                "success":True,
            }
        )
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "success":False,
                "info":e,
            }
        )
        