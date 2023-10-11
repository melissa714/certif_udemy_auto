from django.contrib import admin
from .models import Profile,Location
# Register your models here.


admin.site.site_header = 'Page Administration Melissa_Auto'
admin.site.site_title = 'Admin Melissa_Auto'
admin.site.index_title = 'Admin Melissa_Auto'


class ProfileAdmin(admin.ModelAdmin):
    list_display=["user","bio","phone_number","location","photo"] 
 
    readonly_fields = ('Photo',)

    def thumbnail_preview(self, obj):
        return obj.Photo
    
    thumbnail_preview.short_description = 'Photo'
    thumbnail_preview.allow_tags = True



class LocationAdmin(admin.ModelAdmin):
    list_display=["address_1","address_2","city","state"] 





admin.site.register(Profile,ProfileAdmin)

admin.site.register(Location,LocationAdmin)



class MyModelAdmin(admin.ModelAdmin):
    # ...
    fieldsets = [
        ("Section title", {
            "classes": ("collapse", "expanded"),
            "fields": (...),
        }),
    ]
    # ...