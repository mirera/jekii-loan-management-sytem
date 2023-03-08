from django.contrib import admin
from .models import LoanProduct, Loan, Note

# Register your models here.
admin.site.register(LoanProduct)
admin.site.register(Loan)
admin.site.register(Note)