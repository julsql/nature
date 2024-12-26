from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import AppUser

class AppUserAdmin(UserAdmin):
    model = AppUser

admin.site.register(AppUser, AppUserAdmin)