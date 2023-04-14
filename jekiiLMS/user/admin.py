from django.contrib import admin
from .models import CompanyAdmin, LoginitStaff, SuperAdmin, CompanyStaff, Role

# Register your models here.
admin.site.register(SuperAdmin)
admin.site.register(LoginitStaff)
admin.site.register(CompanyAdmin)
admin.site.register(CompanyStaff)
admin.site.register(Role)

