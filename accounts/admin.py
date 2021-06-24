from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

# # configure admin and custom user model for admin panel 
# + model admin makes password read only
class AccountAdmin(UserAdmin):
# what fields to display on admin panel for quick reference
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'phone_number', 'is_active')
# make fields a link to enter profile clicked
    list_display_links = ('email', 'first_name', 'last_name')
# makes fields read only + if wish not to show password delete from fields below to hide
    readonly_fields = ('last_login', 'date_joined', 'password')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    # profile pic
    def thumbnail(self, object):
        # allows for img
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

# tweeking admin site display/title
admin.site.site_header = 'Vivero Verde Website Admintration'
admin.site.index_title = 'Admin HomePage'
admin.site.site_title = 'Vivero Verde'

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)