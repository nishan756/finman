from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email','username','phone','is_staff','is_active']
    fieldsets = (
        (
            'Authentication Info',
            {
                'fields':('username','email','phone','password')
            }
        ),
        (
            'Club Info',
            {
                'fields':('club_name','established_at','club_logo','details'),
            }
        ),
        (
            'Permissions',
            {
                'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (
            'Important Dates',
            {
                'fields':('date_joined','last_login')
            }
        )

    )

