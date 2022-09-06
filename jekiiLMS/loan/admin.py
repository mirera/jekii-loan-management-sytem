from django.contrib import admin
from .models import LoanProduct, Loan

# Register your models here.
admin.site.register(LoanProduct)
admin.site.register(Loan)