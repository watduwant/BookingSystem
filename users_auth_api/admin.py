from django.contrib import admin

from django.db.models import Q
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile
from django.utils.translation import ugettext_lazy as _


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ('Personal info', {'fields': ('mobile', 'profile_pic', 'status', 'otp', 
                                      'forgot_password')}),
        ('Billing Address', {'fields': ('city', 'address', 'flat_name', 
                                        'landmark', 'pincode')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'get_customer_id', 'get_phone_number', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name', 'get_customer_id', 'get_phone_number', )
    search_fields = ('email', 'first_name', 'last_name', 'profile__customer_id', 'profile__phone_number', 'profile__app_source')
    readonly_fields = ('is_superuser', 'groups', 'user_permissions')
    list_select_related = ('profile', )
    ordering = ('-id',)
    inlines = (UserProfileInline, )


    def get_customer_id(self, instance):
        return instance.profile.customer_id
    get_customer_id.short_description = 'Customer ID'

    def get_phone_number(self, instance):
        return instance.profile.phone_number
    get_phone_number.short_description = 'Phone Number'

