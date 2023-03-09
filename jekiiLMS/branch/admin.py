from django.contrib import admin
from .models import Branch, ExpenseCategory, Expense

# Register your models here.
admin.site.register(Branch)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)