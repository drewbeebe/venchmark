from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Company, User

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
#from .models import MyCustomUser
from rest_framework.authtoken.admin import TokenAdmin
#from .models import User
#from .forms import AddUserForm, UpdateUserForm, NewUserForm, UserAdminCreationForm, UserAdminChangeForm
from .forms import UserAdminCreationForm, UserAdminChangeForm, CompanyAddForm
#from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


#from .forms import UserAdminCreationForm, UserAdminChangeForm
#from .models import User

# Register your models here.
# Vendor Administration
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'is_vendor')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(CompanyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('name',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['owner'] = request.user
        request.GET = data
        return super(CompanyAdmin, self).add_view(request, form_url="", extra_context=extra_context)

admin.site.register(Company, CompanyAdmin)



#class UserAdmin(BaseUserAdmin):
#    form = UpdateUserForm
    #add_form = AddUserForm
#    add_form = NewUserForm

#    list_display = ('email', 'first_name', 'last_name', 'is_staff')
#    list_filter = ('is_staff', )
#    fieldsets = (
#        (None, {'fields': ('email', 'password')}),
#        ('Personal info', {'fields': ('first_name', 'last_name')}),
#        ('Permissions', {'fields': ('is_active', 'is_staff')}),
#    )
#    add_fieldsets = (
#        (
#            None,
#            {
#                'classes': ('wide',),
#                'fields': (
#                    'email', 'first_name', 'last_name', 'password1',
#                    'password2'
#                )
#            }
#        ),
#    )
#    search_fields = ('email', 'first_name', 'last_name')
#    ordering = ('email', 'first_name', 'last_name')
#    filter_horizontal = ()


#admin.site.register(User, UserAdmin)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('email', 'password')
    list_filter = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Roles', {'fields': ['groups']}),
    #    ('Permissions', {'fields': ('admin', 'owner', 'analyst', 'auditor', 'vendor')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
#admin.site.unregister(Group)
