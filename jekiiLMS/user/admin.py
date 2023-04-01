from django.contrib import admin
from .models import CreditOfficer, BranchManager, CompanyAdmin, LoginitStaff, SuperAdmin

# Register your models here.
admin.site.register(SuperAdmin)
admin.site.register(LoginitStaff)
admin.site.register(CompanyAdmin)
admin.site.register(BranchManager)
admin.site.register(CreditOfficer)
