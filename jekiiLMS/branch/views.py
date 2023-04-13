from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Branch ,ExpenseCategory, Expense
from .forms import BranchForm, ExpenseCategoryForm , ExpenseForm
from company.models import Organization
from user.forms import CompanyStaff




#create branch view starts
def createBranch(request):
    form = BranchForm()
    #filter the Branch queryset to include only branches that belong to the logged in company 
    company = request.user.organization
    branches = Branch.objects.filter(company=company)

    #processing the data
    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)
    if request.method == 'POST':
        Branch.objects.create(
            company = company,
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
    context= {
        'form':form,
        'branches' : branches,
        }
    return render(request,'branch/branch-create-form.html', context)
#create branch view ends

#edit branch view starts
def editBranch(request,pk):
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

    branch = Branch.objects.get(id=pk)
    
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        # prepopulate the form with existing data
        form = BranchForm(instance=branch)

    return render(request, 'branch/branch_edit.html', {'form': form})

#edit branch view ends

# list branches view starts 
def list_branches(request):
    #filter the Branch queryset to include only branches that belong to the logged in company 
    company = request.user.organization
    branches = Branch.objects.filter(company=company).order_by('-open_date')
    form = BranchForm()
    

    context = {'branches': branches, 'form':form, }
    return render(request, 'branch/branches_list.html', context)

# list branches view ends

# delete branch view starts 

def deleteBranch(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

    if request.method == 'POST':
        branch = Branch.objects.get(id=pk, company=company)
        branch.delete()

        messages.success(request, 'Branch deleted successfully.')
        return redirect('list')

    return render(request, 'branch/branches_list.html')

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

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)
    #processing the data
    if request.method == 'POST':
        ExpenseCategory.objects.create(
            company = company,
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
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    category = ExpenseCategory.objects.get(id=pk, company=company)
    
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
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    categories = ExpenseCategory.objects.filter(company=company)
    form = ExpenseCategoryForm()
    
    context = {'categories': categories, 'form':form}
    return render(request, 'branch/categories_list.html', context)

# list expense categories view ends

# delete expense category view starts 
def deleteExpenseCategory(request,pk):
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    category = ExpenseCategory.objects.get(id=pk, company=company)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Branch deleted successfully.')
        return redirect('expense-categories')

    context = {'obj':category}
    return render(request,'branch/categories_list.html', context)

# delete expense category view ends 



#create expense category view starts
def createExpense(request):
    form = ExpenseForm()
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # Get the selected category id from the form
        category_id = request.POST.get('category')
        category = ExpenseCategory.objects.get(pk=category_id)

        # Get the selected branch id from the form
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(pk=branch_id)

        # Get the selected user id from the form
        created_by = request.user

        Expense.objects.create(
            company = company,
            expense_date = request.POST.get('expense_date'),
            category = category,
            amount = request.POST.get('amount'),
            branch = branch,
            created_by = created_by,
            note = request.POST.get('note'),
            attachement = request.FILES.get('attachement'),
        )
        messages.success(request, 'Expense added successfully!')
        return redirect('expenses')
    context= {'form':form}
    return render(request,'branch/expenses_list.html', context)
#create expense category view ends  


# list expense Categories view starts 
def list_expenses(request):
    expenses = Expense.objects.all()
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    expenses = Expense.objects.filter(company=company)
    form = ExpenseForm()

    context = {'expenses': expenses, 'form':form}
    return render(request, 'branch/expenses_list.html', context)

# list expense categories view ends


#edit expense category view starts
def editExpense(request,pk):
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user) 

    expense = Expense.objects.get(id=pk, company=company)
    
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
        return render(request,'branch/expenses_list.html',{'form':form})

#edit expense category view ends  


# delete expense  view starts 
def deleteExpense(request,pk):
    company = request.user.organization

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        company = Organization.objects.get(admin=user)

    expense = Expense.objects.get(id=pk, company=company)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Branch deleted successfully.')
        return redirect('expenses')

    context = {'obj':expense}
    return render(request,'branch/expenses_list.html', context)

# delete expense  view ends 