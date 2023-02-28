from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Branch
from .forms import BranchForm




#create branch view starts
def createBranch(request):
    form = BranchForm()
    #processing the data
    if request.method == 'POST':
        Branch.objects.create(
            name = request.POST.get('name'),
            phone= request.POST.get('phone'),
            email = request.POST.get('email'),
            capital = request.POST.get('capital'),
            office = request.POST.get('office'),
            open_date = request.POST.get('open_date'),
            notes = request.POST.get('notes'),
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('list')
    context= {'form':form}
    return render(request,'branch/branch-create-form.html', context)
#create branch view ends

#edit branch view starts
def editBranch(request,pk):
    branch = Branch.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        branch.name = request.POST.get('name')
        branch.office = request.POST.get('office')
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
            'office': branch.office,
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

# list branches view ends

# delete branch view starts 
def deleteBranch(request,pk):
    branch = Branch.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        branch.delete()
        return redirect('list')

        messages.success(request, 'Branch deleted successfully.')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':branch}
    return render(request,'branch/delete_branch.html', context)

# delete branch ends starts


# view branch view starts 
def viewBranch(request, pk):
    branch = Branch.objects.get(id=pk)

    context = {'branch': branch}
    return render(request, 'branch/branch.html', context)

# view branch view ends