from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Branch ,ExpenseCategory, Expense
from .forms import BranchForm, ExpenseCategoryForm , ExpenseForm




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
    form = BranchForm()
    

    context = {'branches': branches, 'form':form, }
    return render(request, 'branch/branches_list.html', context)

# list branches view ends

# delete branch view starts 

def deleteBranch(request,pk):
    branch = Branch.objects.get(id=pk)
    branch.delete()

    context = {'branch':branch}
    messages.success(request, 'Branch deleted successfully.')
    return redirect('list')

# delete branch ends starts


# view branch view starts 
def viewBranch(request, pk):
    branch = Branch.objects.get(id=pk)

    context = {'branch': branch}
    return render(request, 'branch/branch.html', context)

# view branch view ends


#create expense category view starts
def createExpenseCategory(request):
    form = ExpenseCategoryForm()
    #processing the data
    if request.method == 'POST':
        ExpenseCategory.objects.create(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('expense-categories')
    context= {'form':form}
    return render(request,'branch/create-expensecategory.html', context)
#create expense category view ends

#edit expense category view starts
def editCategory(request,pk):
    category = ExpenseCategory.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()

        return redirect('expense-categories')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': category.name,
            'description': category.description
        }
        form = ExpenseCategoryForm(initial=form_data)
        return render(request,'branch/expense-category-edit.html',{'form':form})

#edit expense category view ends

# list expense Categories view starts 
def list_categories(request):
    categories = ExpenseCategory.objects.all()
    form = ExpenseCategoryForm()

    context = {'categories': categories, 'form':form}
    return render(request, 'branch/categories_list.html', context)

# list expense categories view ends

# delete expense category view starts 
def deleteExpenseCategory(request,pk):
    category = ExpenseCategory.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        category.delete()
        return redirect('expense-categories')

        messages.success(request, 'Branch deleted successfully.')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':category}
    return render(request,'branch/delete-category.html', context)

# delete expense category view ends 



#create expense category view starts
def createExpense(request):
    form = ExpenseForm()
    #processing the data
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # Get the selected category id from the form
        category_id = request.POST.get('category')
        
        # Get the corresponding ExpenseCategory object
        category = ExpenseCategory.objects.get(pk=category_id)

        # Get the selected branch id from the form
        branch_id = request.POST.get('branch')
        
        # Get the corresponding Branch object
        branch = Branch.objects.get(pk=branch_id)

        # Get the selected user id from the form
        #creator_id = request.POST.get('created_by')
        
        # Get the corresponding user object
        #created_by = User.objects.get(pk=creator_id)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.attachement = request.FILES.get('attachement')
            expense.save()
            return redirect('expenses')
        '''
        Expense.objects.create(
            expense_date = request.POST.get('expense_date'),
            category = category,
            amount = request.POST.get('amount'),
            branch = branch,
            created_by = created_by,
            note = request.POST.get('note'),
            attachement = request.FILES.get('attachement'),
        )
        '''
        #redirecting user to branches page(url name) after submitting form
        #return redirect('expenses')
    context= {'form':form}
    return render(request,'branch/create-expense.html', context)
#create expense category view ends  


# list expense Categories view starts 
def list_expenses(request):
    expenses = Expense.objects.all()
    form = ExpenseForm()

    context = {'expenses': expenses, 'form':form}
    return render(request, 'branch/expenses_list.html', context)

# list expense categories view ends


#edit expense category view starts
def editExpense(request,pk):
    expense = Expense.objects.get(id=pk)
    
    if request.method == 'POST':
        # Get the selected category id from the form
        category_id = request.POST.get('category')
        
        # Get the corresponding ExpenseCategory object
        category = ExpenseCategory.objects.get(pk=category_id)

        # Get the selected branch id from the form
        branch_id = request.POST.get('branch')
        
        # Get the corresponding Branch object
        branch = Branch.objects.get(pk=branch_id)

        # update the branch with the submitted form data
        expense.expense_date = request.POST.get('expense_date')
        expense.category = category
        expense.amount = request.POST.get('amount')
        expense.branch = branch
        expense.note = request.POST.get('note')
        expense.attachement = request.FILES.get('attachement')
        expense.save()

        return redirect('expenses')
    else:
        # prepopulate the form with existing data
        form_data = {
            'expense_date': expense.expense_date,
            'category': expense.category,
            'amount': expense.amount,
            'branch': expense.branch,
            'note': expense.note,
            'attachement': expense.attachement,
        }
        form = ExpenseForm(initial=form_data)
        return render(request,'branch/expense-edit.html',{'form':form})

#edit expense category view ends  


# delete expense  view starts 
def deleteExpense(request,pk):
    expense = Expense.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses')

        messages.success(request, 'Branch deleted successfully.')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':expense}
    return render(request,'branch/delete-expense.html', context)

# delete expense  view ends 