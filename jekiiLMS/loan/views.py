from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User
from .models import LoanProduct, Loan, Note, Repayment, Guarantor, Collateral
from .forms import LoanProductForm, LoanForm, RepaymentForm, GuarantorForm, CollateralForm
from member.models import Member






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
    form = LoanProductForm()

    context = {'loanproducts': loanproducts, 'form':form}
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
        # Get the selected loanproduct id from the form
        loanproduct_id = request.POST.get('loan_product')
        
        # Get the corresponding LoanProduct object
        loanproduct = LoanProduct.objects.get(pk=loanproduct_id)

        # Get the selected member id from the form
        member_id = request.POST.get('member')
        
        # Get the corresponding Member object
        member = Member.objects.get(pk=member_id)
      
        # Get the selected member id from the form
        loan_officer_id = request.POST.get('loan_officer')
        
        # Get the corresponding Member object
        loan_officer = User.objects.get(pk=loan_officer_id)

        if member.has_active_loan():
            # redirect to an error page or show an error message
            #messages.error(request, 'This Member has an active loan!')
            return render(request, 'loan/error.html', {'message': 'You cannot apply for a new loan while you have an active loan.'})

        Loan.objects.create(
             loan_product= loanproduct,
             member= member,
             applied_amount = request.POST.get('applied_amount'),
             application_date = request.POST.get('application_date'),
             loan_officer = loan_officer,
             loan_purpose = request.POST.get('loan_purpose'),
             attachments = request.FILES.get('attachments'),
         )
        #redirecting user to branches page(url name) after submitting form
        messages.success(request, 'Loan created successfully!')
        return redirect('loans')
 
    context= {'form':form}
    return render(request,'loan/loan-create.html', context)
#create loan view ends

#edit Loan  view starts
def editLoan(request,pk):
    loan = Loan.objects.get(id=pk)
    
    if request.method == 'POST':
        # Get the selected loanproduct id from the form
        loanproduct_id = request.POST.get('loan_product')
        
        # Get the corresponding LoanProduct object
        try:
            loanproduct = LoanProduct.objects.get(pk=loanproduct_id)
        except LoanProduct.DoesNotExist:
            loanproduct = None
        # Get the selected member id from the form
        member_id = request.POST.get('member')
        
        # Get the corresponding Member object
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            member = None

        # Get the selected member id from the form
        loan_officer_id = request.POST.get('loan_officer')
        
        # Get the corresponding Member object
        try:
            loan_officer = User.objects.get(pk=loan_officer_id)
        except User.DoesNotExist:
            loan_officer = None

        # update the branch with the submitted form data
        loan.loan_id = request.POST.get('loan_id')
        loan.loan_product = loanproduct
        loan.member = member
        loan.applied_amount = request.POST.get('applied_amount')
        loan.application_date = request.POST.get('application_date')
        loan.loan_officer = loan_officer
        loan.loan_purpose = request.POST.get('loan_purpose')
        loan.attachments = request.FILES.get('attachments')

        loan.save()

        return redirect('loans')
    else:
        # prepopulate the form with existing data
        form_data = {
            'loan_id': loan.loan_id,
            'loan_product': loan.loan_product,
            'member': loan.member,
            'applied_amount': loan.applied_amount,
            'application_date': loan.application_date,
            'loan_officer': loan.loan_officer,
            'loan_purpose': loan.loan_purpose,
            'attachments': loan.attachments
        }
        form = LoanForm(initial=form_data)
        return render(request,'loan/edit-loan.html',{'form':form})

#edit Loan view ends

#approve loan logic starts here
def approveLoan(request,pk):
    if request.method == 'POST':
        loan = Loan.objects.get(id=pk)
        # Get the URL pattern for the 'view-loan' view
        url = reverse('view-loan', args=[pk])
        # Append the anchor to the end of the URL
        url_with_anchor = f'{url}'

        if loan.status == 'pending':
            loan.status = 'approved'
            loan.save()
            messages.success(request,'The loan was approved succussesfully!')
            return redirect(url_with_anchor)
    return render(request,'loan/loans-list.html')
#approve logic ends

#approve loan logic starts here
def rejectLoan(request,pk):
    if request.method == 'POST':
        loan = Loan.objects.get(id=pk)
        url = reverse('view-loan', args=[pk])
        url_with_anchor = f'{url}'
        if loan.status == 'pending':
            loan.status = 'rejected'
            loan.save()
            messages.info(request,'The loan was rejected succussesfully!')
            return redirect(url_with_anchor)
    return render(request,'loan/loans-list.html')
#approve logic ends

# list Loan  view starts 
def listLoans(request):
    loans = Loan.objects.all()
    form = LoanForm()

    context = {'loans': loans, 'form':form}
    return render(request, 'loan/loans-list.html', context)

# list Loan  view ends


# detailview Loan  view starts 
def viewLoan(request, pk):
    loan = Loan.objects.get(id=pk)
    loan_notes = loan.note_set.all().order_by('-created')
    guarantors = Guarantor.objects.filter(loan=loan)
    collaterals = Collateral.objects.filter(loan=loan)
    repayments = Repayment.objects.filter(loan_id=loan)
    form = GuarantorForm()
    form_collateral = CollateralForm()
    form_repayment = RepaymentForm()

    #a sum of all repayments made toward a specifi loan 
    loan_repayments = Repayment.objects.filter(loan_id=loan.id).aggregate(Sum('amount'))['amount__sum']
    #loan balance
    total_payable= loan.total_payable()
    if loan_repayments:
        if total_payable:
            loan_balance= total_payable-loan_repayments
        else:
            loan_balance = 0
    else:
        loan_balance = total_payable

    if request.method == 'POST':
        Note.objects.create(
            author = request.user,
            loan = loan,
            body = request.POST.get('body')
        )
        return redirect('view-loan', pk=loan.id)

    context = {
        'loan_notes': loan_notes,
        'loan':loan,
        'loan_repayments':loan_repayments,
        'loan_balance':loan_balance,
        'form':form,
        'guarantors':guarantors,
        'repayments':repayments,
        'collaterals':collaterals,
        'form_collateral':form_collateral,
        'form_repayment':form_repayment
        }
    return render(request, 'loan/loan-view.html', context)

# detailview Loan  view ends


# delete Loan  view starts 
def deleteLoan(request,pk):
    loan = Loan.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        loan.delete()
        return redirect('loans')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':loan}
    return render(request,'loan/delete-loan.html', context)

# delete Loan  ends starts


#create repayment view starts
def createRepayment(request):
    form = RepaymentForm()
    #processing the data
    if request.method == 'POST':
        # Get the selected member id from the form
        member_id = request.POST.get('member')
        
        # Get the corresponding Member object
        member = Member.objects.get(pk=member_id)

        # Get the selected loanproduct id from the form
        loan_id = request.POST.get('loan_id')
        
        # Get the corresponding LoanProduct object
        loan = Loan.objects.get(pk=loan_id)
        Repayment.objects.create(
            transaction_id= request.POST.get('transaction_id'),
            loan_id = loan,
            member = member,
            amount= request.POST.get('amount'),
            date_paid = request.POST.get('date_paid'),
        )
        #redirecting user to Repayments page(url name) after submitting form
        return redirect('repayments')
 
    context= {'form':form}
    return render(request,'loan/repayment-create.html', context)
#create loan view ends

# list Repayments  view starts 
def listRepayments(request):
    repayments = Repayment.objects.all()
    form = RepaymentForm()

    context = {'repayments': repayments, 'form':form}
    return render(request, 'loan/repayment-list.html', context)

# list Repayment  view ends

# delete Repayment  view starts 
def deleteRepayment(request,pk):
    repayment = Repayment.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        repayment.delete()
        return redirect('repayments')


     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':repayment}
    return render(request,'loan/delete-repayment.html', context)

# delete Repayment  ends 

#edit repayment  view starts
def editRepayment(request,pk):
    repayment = Repayment.objects.get(id=pk)
    
    if request.method == 'POST':

        # Get the selected member id from the form
        member_id = request.POST.get('member')
        
        # Get the corresponding Member object
        member = Member.objects.get(pk=member_id)

        # Get the selected loanproduct id from the form
        loan_id = request.POST.get('loan_id')
        
        # Get the corresponding LoanProduct object
        loan = Loan.objects.get(pk=loan_id)

        # update the branch with the submitted form data
        repayment.loan_id = loan
        repayment.transaction_id = request.POST.get('transaction_id')
        repayment.member = member
        repayment.amount = request.POST.get('amount')
        repayment.date_paid = request.POST.get('date_paid')
        repayment.save()

        return redirect('repayments')
    else:
        # prepopulate the form with existing data
        form_data = {
            'loan_id': repayment.loan_id,
            'member': repayment.member,
            'amount': repayment.amount,
            'transaction_id': repayment.transaction_id,
            'date_paid': repayment.date_paid
        }
        form = RepaymentForm(initial=form_data)
        return render(request,'loan/edit-repayment.html',{'form':form})

#edit repayment view ends
 
#loan cacl view start

def loan_calculator(request):
    if request.method == "POST":
        loan_product_id = request.POST.get("loan_product")
        amount = float(request.POST.get("amount"))
        loan_product = LoanProduct.objects.get(id=loan_product_id)

        interest_rate = loan_product.interest_rate
        interest_type = loan_product.interest_type
        loan_term = loan_product.loan_product_term

        amount_to_pay = 0
        total_interest = 0

        if interest_type == 'flat rate':
            interest_rate = loan_product.interest_rate / 100
            total_interest = amount * interest_rate * loan_term
            total_payable = amount + total_interest 
            amount_to_pay = total_payable / loan_term
        else:
            interest_rate = loan_product.interest_rate / 100
            payment_amount = (interest_rate * amount) / (1 - (1 + interest_rate)**(-loan_term))
            total_payable = payment_amount * loan_term
            

        table_data = []
        for i in range(loan_term):
            principal_amount = amount_to_pay * (i+1)
            interest_per_term = total_interest / loan_term
            principal_per_term = amount / loan_term
            amount_per_term = interest_per_term + principal_per_term
            loan_balance = principal_amount - amount_per_term
            table_data.append({
                "principal_amount": principal_amount,
                "total_payable": total_payable,
                "amount_to_pay": amount_to_pay,
                'principal_per_term': principal_per_term,
                'interest_per_term':interest_per_term,
                'amount_per_term': amount_per_term,
                'loan_balance': loan_balance,
            })

        context = {
            "loanproducts": LoanProduct.objects.all(),
            "table_data": table_data
        }

        return render(request, "loan/loan-calculator.html", context)

    context = {
        "loanproducts": LoanProduct.objects.all(),
        "table_data": []
    }
    return render(request, "loan/loan-calculator.html", context)
#loan cacl view ends

#add guarontor view starts
def addGuarantor(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    form = GuarantorForm()
    guarantor_id = request.POST.get('name')
    guarantor = Member.objects.get(id=guarantor_id)

    if request.method == 'POST':
        form = GuarantorForm(request.POST)

        Guarantor.objects.create(
            loan = loan,
            name = guarantor,
            amount = request.POST.get('amount')
        )
        messages.success(request, 'Guarantor added successfully.')
        return redirect('view-loan', pk=loan.id)
       
    context= {'form':form, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
#dd guarontor view ends   

#remove guarantor view
# delete Repayment  view starts 
def removeGuarantor(request,pk):
    guarantor = Guarantor.objects.get(id=pk)
#include a functionality to limit any user from deleteng this objec unless they have admin previleges
    if request.method == 'POST':
        guarantor.delete()
        return redirect('repayments')
     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':guarantor}
    return render(request,'loan/delete-repayment.html', context)

# delete Repayment  ends 


#add guarontor view starts
def addCollateral(request, pk):
    loan = Loan.objects.get(pk=pk)
    form = CollateralForm()
    #processing the data
    if request.method == 'POST':
        form = CollateralForm(request.POST)
        # Get the URL pattern for the 'view-loan' view
        url = reverse('view-loan', args=[pk])

        # Append the anchor to the end of the URL
        url_with_anchor = f'{url}#tabItem18'

        if form.is_valid():
            collateral = form.save(commit=False)
            collateral.loan = loan
            collateral.save()
            #redirecting user to view loan page with loan id
            messages.success(request, 'Collateral added successfully.')
            #return redirect('view-loan', pk=loan_id)
            return redirect(url_with_anchor)
 
    context= {'form':form}
    return render(request,'loan/loan-view.html', context)
#dd guarontor view ends   



#add guarontor view starts
def editCollateral(request,pk):
    collateral = Collateral.objects.get(id=pk)
    #processing the data
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = Loan.objects.get(pk=loan_id)

        # Get the URL pattern for the 'view-loan' view
        url = reverse('view-loan', args=[loan_id])

        # Append the anchor to the end of the URL
        url_with_anchor = f'{url}#tabItem18'

        collateral.loan_id = loan
        collateral.name = request.POST.get('name')
        collateral.type = request.POST.get('type')
        collateral.serial_number = request.POST.get('serial_number')
        collateral.estimated_value = request.POST.get('estimated_value')
        collateral.save()
        
        messages.success(request, 'Collateral saved successfully.')
        #return redirect('view-loan', pk=loan_id)
        return redirect(url_with_anchor)
    else:
        # prepopulate the form with existing data
        form_data = {
            'loan_id': collateral.loan_id,
            'name': collateral.name,
            'type': collateral.type,
            'serial_number': collateral.serial_number,
            'estimated_value': collateral.estimated_value
        }
        form = CollateralForm(initial=form_data)
        context= {'form':form}
        return render(request,'loan/loan-view.html', context)
 
#edit collateral view ends  

  