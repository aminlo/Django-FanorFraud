from django.contrib import admin
from .models import CustomUser

# Register the CustomUser model with the admin
admin.site.register(CustomUser)