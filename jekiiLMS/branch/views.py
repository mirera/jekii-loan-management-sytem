from django.shortcuts import render, redirect
from .models import Branch
from .forms import BranchForm




#create branch view starts
def createBranch(request):
    
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

    return render(request,'branch/branch-create-form.html')
#create branch view ends

#edit branch view starts
def editBranch(request,pk):
    branch = Branch.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        branch.name = request.POST.get('name')
        branch.phone = request.POST.get('phone')
        branch.email = request.POST.get('email')
        branch.open_date = request.POST.get('open_date')
        branch.capital = request.POST.get('capital')
        branch.status = request.POST.get('status')
        branch.notes = request.POST.get('notes')
        branch.save()

        return redirect('list')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': branch.name,
            'phone': branch.phone,
            'email': branch.email,
            'open_date': branch.open_date,
            'capital': branch.capital,
            'status': branch.status,
            'notes': branch.notes
        }
        form = BranchForm(initial=form_data)
        return render(request,'branch/branch_edit.html',{'form':form})

#edit branch view ends

# list branches view starts 
def list_branches(request):
    branches = Branch.objects.all().order_by('-open_date')

    context = {'branches': branches}
    return render(request, 'branch/branches_list.html', context)

# list branches view starts