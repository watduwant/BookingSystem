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
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'get_customer_id', 'get_phone_number', 'get_app_source', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name', 'get_customer_id', 'get_phone_number', 'get_app_source')
    search_fields = ('email', 'first_name', 'last_name', 'profile__customer_id', 'profile__phone_number', 'profile__app_source')
    readonly_fields = ('is_superuser', 'groups', 'user_permissions')
    list_select_related = ('profile', )
    ordering = ('-id',)
    inlines = (UserProfileInline, )

    # def get_queryset(self, request):
    #     qs = super(UserAdmin, self).get_queryset(request)
        # if request.user.profile.belongs_to == 'ifl_services':
        #     return qs.filter(Q(profile__belongs_to='ifl_services'))
        # elif request.user.profile.belongs_to == 'EquityGlobal':
        #     return qs.filter(Q(profile__belongs_to='EquityGlobal'))

    def get_customer_id(self, instance):
        return instance.profile.customer_id
    get_customer_id.short_description = 'Customer ID'

    def get_phone_number(self, instance):
        return instance.profile.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_app_source(self, instance):
        return instance.profile.app_source
    get_app_source.short_description = 'App Source'

    # def get_permissions(self, instance):
    #     return instance.profile.permissions
    # get_permissions.short_description = 'Permissions'

