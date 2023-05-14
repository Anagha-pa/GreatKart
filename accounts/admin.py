# from django.contrib import admin
# from .models import CustomUser

# # Register your models here.
# admin.site.register(CustomUser)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import CustomUser,UserProfile
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class UserProfileAdmin(admin.ModelAdmin):
    
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%">'.format(object.profile_picture.url))
        thumbnail.short_description = 'profile_picture'
    list_display = ('thumbnail','user', 'city', 'state', 'country')    



admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)