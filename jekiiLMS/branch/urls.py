from django.urls import path
from . import views


urlpatterns = [
    #branch urls
    path('list', views.list_branches, name='list'),
    path('create', views.createBranch, name='create'),
    path('edit/<str:pk>', views.editBranch, name='edit'),
    path('view/<str:pk>', views.viewBranch, name='view'),
    path('delete/<str:pk>', views.deleteBranch, name='delete'),

    #category urls
    path('expense-categories', views.list_categories, name='expense-categories'),
    path('create-exp-cat', views.createExpenseCategory, name='create-exp-cat'),
    path('edit-exp-cat/<str:pk>', views.editCategory, name='edit-exp-cat'),
    path('delete-exp-cat/<str:pk>', views.deleteExpenseCategory, name='delete-exp-cat'),

    #expense urls
    path('expenses', views.list_expenses, name='expenses'),
    path('create-expense', views.createExpense, name='create-expense'),
    path('edit-expense/<str:pk>', views.editExpense, name='edit-expense'),
    path('delete-expense/<str:pk>', views.deleteExpense, name='delete-expense'),
]  