from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('owner_name', 'state', 'school_name', 'phone_number')}),
        ('Status', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'owner_name', 'state', 'school_name', 'phone_number'),
        }),
    )
    list_display = ('username', 'email', 'owner_name', 'is_active')
    search_fields = ('username', 'email', 'owner_name')
    ordering = ('username',)

admin.site.register(User, UserAdmin)