from django.contrib import admin
from .models import LoanProduct, Loan, Note, Repayment

# Register your models here.
admin.site.register(LoanProduct)
admin.site.register(Loan)
admin.site.register(Note) 
admin.site.register(Repayment)