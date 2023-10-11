from django.contrib import admin
from .models import Listing,LikedListing
# Register your models here.



admin.site.site_header = 'Page Administration Melissa_Auto'
admin.site.site_title = 'Admin Melissa_Auto'
admin.site.index_title = 'Admin Melissa_Auto'



class ListingAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at", "seller", "brand","model","color","image"]
    search_fields=["id", "created_at", "updated_at", "seller", "brand","model","color","image"]
    readonly_fields=('id',)
    
    readonly_fields = ('image_view',)

    def thumbnail_preview(self, obj):
        return obj.image_view


    

class LikedListingAdmin(admin.ModelAdmin):
    list_display = ["profile", "listing", "like_date"]
    search_fields=["profile", "listing", "like_date",]
    readonly_fields=('id',)

admin.site.register(Listing,ListingAdmin)


admin.site.register(LikedListing,LikedListingAdmin)


