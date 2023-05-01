from django.contrib import admin
from .models import Organization, Package

# Register your models here.
admin.site.register(Organization)
admin.site.register(Package)