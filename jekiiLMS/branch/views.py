from django.shortcuts import render, redirect
from .models import Branch
from .forms import BranchForm



#create a branch
def createBranch(request):
    form = BranchForm()
    
    #processing the data
    if request.method == 'POST':

        Branch.objects.create(
            name = request.POST.get('name'),
            phone= request.POST.get('phone'),
            email = request.POST.get('email'),
            capital = request.POST.get('capital'),
            open_date = request.POST.get('open_date'),
            notes = request.POST.get('notes'),
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('list')

    context = {"form":form} 
    return render(request,'branch/branch-create-form.html', context)

# View to list all available branches
def list_branches(request):
    branches = Branch.objects.all().order_by('-open_date')

    context = {'branches': branches}
    return render(request, 'branch/branches_list.html', context)
