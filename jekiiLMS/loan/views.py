from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoanProduct, Loan
from .forms import LoanProductForm, LoanForm





#create Loan Product view starts
def createLoanProduct(request):
    form = LoanProductForm()
    #processing the data
    if request.method == 'POST':
        LoanProduct.objects.create(
            loan_product_name = request.POST.get('loan_product_name'),
            minimum_amount= request.POST.get('minimum_amount'),
            maximum_amount= request.POST.get('maximum_amount'),
            loan_product_term = request.POST.get('loan_product_term'),
            loan_term_period = request.POST.get('loan_term_period'),
            repayment_frequency = request.POST.get('repayment_frequency'),
            interest_type = request.POST.get('interest_type'),
            interest_rate = request.POST.get('interest_rate'),
            service_fee_type = request.POST.get('service_fee_type'),
            service_fee_value = request.POST.get('service_fee_value'),
            penalty_type = request.POST.get('penalty_type'),
            penalty_value = request.POST.get('penalty_value'),
            penalty_frequency = request.POST.get('penalty_frequency'),
            loan_product_description = request.POST.get('loan_product_description'),
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('loan-products')

    loanproducts = LoanProduct.objects.all() #this loanproducts context is added to form conext because of {{loanproducts.count}} in the sidebar 
    context= {'form':form,'loanproducts':loanproducts }
    return render(request,'loan/loan-product-create.html', context)
#create loan Product view ends


# list Loan Products view starts 
def listLoanProducts(request):
    loanproducts = LoanProduct.objects.all()

    context = {'loanproducts': loanproducts}
    return render(request, 'loan/loan-product-list.html', context)

# list Loan Products view ends

# detailview Loan Products view starts 
def viewLoanProduct(request, pk):
    loanproduct = LoanProduct.objects.get(id=pk)

    context = {'loanproduct': loanproduct}
    return render(request, 'loan/loan-product-view.html', context)

# detailview Loan Products view ends

# delete Loan Products view starts 
def deleteLoanProduct(request,pk):
    loanproduct = LoanProduct.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        loanproduct.delete()
        return redirect('loan-products')

        messages.success(request, 'Branch deleted successfully.')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':loanproduct}
    return render(request,'loan/delete-loan-product.html', context)

# delete Loan Products ends starts

#edit Loan Products view starts
def editLoanProduct(request,pk):
    loanproduct = LoanProduct.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        loanproduct.loan_product_name = request.POST.get('loan_product_name')
        loanproduct.minimum_amount= request.POST.get('minimum_amount')
        loanproduct.maximum_amount= request.POST.get('maximum_amount')
        loanproduct.loan_product_term = request.POST.get('loan_product_term')
        loanproduct.loan_term_period = request.POST.get('loan_term_period')
        loanproduct.repayment_frequency = request.POST.get('repayment_frequency')
        loanproduct.interest_type = request.POST.get('interest_type')
        loanproduct.interest_rate = request.POST.get('interest_rate')
        loanproduct.service_fee_type = request.POST.get('service_fee_type')
        loanproduct.service_fee_value = request.POST.get('service_fee_value')
        loanproduct.penalty_type = request.POST.get('penalty_type')
        loanproduct.penalty_value = request.POST.get('penalty_value')
        loanproduct.penalty_frequency = request.POST.get('penalty_frequency')
        loanproduct.loan_product_description = request.POST.get('loan_product_description')

        loanproduct.save()

        return redirect('loan-products')
    else:
        # prepopulate the form with existing data
        form_data = {
            'loan_product_name': loanproduct.loan_product_name,
            'minimum_amount':loanproduct.minimum_amount,
            'maximum_amount':loanproduct.maximum_amount,
            'loan_product_term':loanproduct.loan_product_term,
            'loan_term_period':loanproduct.loan_term_period,
            'repayment_frequency':loanproduct.repayment_frequency,
            'interest_type':loanproduct.interest_type,
            'interest_rate':loanproduct.interest_rate,
            'service_fee_type':loanproduct.service_fee_type,
            'service_fee_value':loanproduct.service_fee_value,
            'penalty_type':loanproduct.penalty_type,
            'penalty_value':loanproduct.penalty_value,
            'penalty_frequency':loanproduct.penalty_frequency,
            'status':loanproduct.status,
            'loan_product_description':loanproduct.loan_product_description
        }
        form = LoanProductForm(initial=form_data)
        return render(request,'loan/edit-loan-product.html',{'form':form})

#edit Loan Products view ends




#views for loan 

#create Loan view starts
def createLoan(request):
    form = LoanForm()
    #processing the data
    if request.method == 'POST':
        Loan.objects.create(
            loan_id = request.POST.get('loan_id'),
            loan_product= request.POST.get('loan_product'),
            member= request.POST.get('member'),
            applied_amount = request.POST.get('applied_amount'),
            guarantor = request.POST.get('guarantor'),
            application_date = request.POST.get('application_date'),
            loan_officer = request.POST.get('loan_officer'),
            loan_purpose = request.POST.get('loan_purpose'),
            attachments = request.POST.get('attachments'),
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('loans')
 
    context= {'form':form}
    return render(request,'loan/loan-create.html', context)
#create loan view ends

#edit Loan  view starts
def editLoan(request,pk):
    loan = Loan.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        loan.loan_id = request.POST.get('loan_id')
        loan.loan_product = request.POST.get('loan_product')
        loan.member = request.POST.get('member')
        loan.applied_amount = request.POST.get('applied_amount')
        loan.guarantor = request.POST.get('guarantor')
        loan.application_date = request.POST.get('application_date')
        loan.loan_officer = request.POST.get('loan_officer')
        loan.loan_purpose = request.POST.get('loan_purpose')
        loan.status = request.POST.get('status')
        loan.attachments = request.POST.get('attachments')

        loan.save()

        return redirect('loans')
    else:
        # prepopulate the form with existing data
        form_data = {
            'loan_id': loan.loan_id,
            'loan_product': loan.loan_product,
            'member': loan.member,
            'applied_amount': loan.applied_amount,
            'guarantor': loan.guarantor,
            'application_date': loan.application_date,
            'loan_officer': loan.loan_officer,
            'loan_purpose ': loan.loan_purpose ,
            'status': loan.status,
            'attachments': loan.attachments,
        }
        form = LoanForm(initial=form_data)
        return render(request,'loan/edit-loan.html',{'form':form})

#edit Loan view ends

# list Loan  view starts 
def listLoans(request):
    loans = Loan.objects.all()

    context = {'loans': loans}
    return render(request, 'loan/loans-list.html', context)

# list Loan  view ends