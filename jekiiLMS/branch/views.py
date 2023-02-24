from django.shortcuts import render, redirect
from .models import Branch

# View to list all available branches
def list_branches(request):
    branches = Branch.objects.all().order_by('-open_date')

    context = {'branches': branches}
    return render(request, 'branch/branches_list.html', context)
