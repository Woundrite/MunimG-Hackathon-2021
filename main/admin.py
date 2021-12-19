from django.contrib import admin
# from .models import UserProfile
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# admin.site.register(UserProfile)
admin.site.register(User)