from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
import os
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.models import User
from jekiiLMS.decorators import role_required
from .models import LoanProduct, Loan, Note, Repayment, Guarantor, Collateral, MpesaStatement
from .forms import LoanProductForm, LoanForm, RepaymentForm, GuarantorForm, CollateralForm, MpesaStatementForm
from member.models import Member
from company.models import Organization
from user.models import CompanyStaff
from jekiiLMS.process_loan import is_sufficient_collateral, calculate_loan_amount, get_amount_to_disburse, clear_loan, update_member_data
from jekiiLMS.mpesa_statement import get_loans_table


#create Loan Product view starts 
#@role_required
def createLoanProduct(request):
    form = LoanProductForm()

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        

    if request.method == 'POST':
        LoanProduct.objects.create(
            company = company,
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
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loanproducts = LoanProduct.objects.filter(company=company)
    form = LoanProductForm()

    context = {'loanproducts': loanproducts, 'form':form}
    return render(request, 'loan/loan-product-list.html', context)

# list Loan Products view ends

# detailview Loan Products view starts 
def viewLoanProduct(request, pk):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loanproduct = LoanProduct.objects.get(id=pk, company=company)

    context = {'loanproduct': loanproduct}
    return render(request, 'loan/loan-product-view.html', context)

# detailview Loan Products view ends

# delete Loan Products view starts 
#@role_required
def deleteLoanProduct(request,pk):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loanproduct = LoanProduct.objects.get(id=pk, company=company)
    if request.method == 'POST':
        loanproduct.delete()
        messages.success(request, 'Branch deleted successfully.')
        return redirect('loan-products')
    context = {'obj':loanproduct}
    return render(request,'loan/delete-loan-product.html', context)

# delete Loan Products ends starts 

#edit Loan Products view starts
#@role_required
def editLoanProduct(request,pk):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loanproduct = LoanProduct.objects.get(id=pk, company=company)
    
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
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
    
    form = LoanForm(request.POST, company=company) #instiated the two kwargs to be able to access them on the forms.py
    #processing the data
    if request.method == 'POST':
        loanproduct_id = request.POST.get('loan_product')
        loanproduct = LoanProduct.objects.get(pk=loanproduct_id)

        member_id = request.POST.get('member')
        member = Member.objects.get(pk=member_id)

        loan_officer_id = request.POST.get('loan_officer')
        loan_officer = CompanyStaff.objects.get(pk=loan_officer_id)

        if member.has_active_loan():
            return render(request, 'loan/error.html', {'message': 'You cannot apply for a new loan while you have an active loan.'})

        Loan.objects.create(
                company = company,
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
    return render(request,'loan/loans-list.html', context)
#create loan view ends

#edit Loan  view starts
def editLoan(request,pk):
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
    
    loan = Loan.objects.get(id=pk, company=company)
    
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

        loan_officer_id = request.POST.get('loan_officer')
        loan_officer = CompanyStaff.objects.get(pk=loan_officer_id)

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
        form = LoanForm(initial=form_data, company=company)
        return render(request,'loan/edit-loan.html',{'form':form})

#edit Loan view ends

#approve loan logic starts here
#@role_required
def approveLoan(request,pk):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_active:
            try:
                companystaff = CompanyStaff.objects.get(username=request.user.username)
                company = companystaff.company
            except CompanyStaff.DoesNotExist:
                company = None
        else:
            company = None
        
        loan = Loan.objects.get(id=pk, company=company)
        borrower = loan.member
        guarantors = Guarantor.objects.filter(loan=loan)
        today = datetime.today().strftime('%Y-%m-%d')

        guarantors_score = 0
        for guarantor in guarantors:
            guarantors_score += guarantor.name.credit_score

        member_score = borrower.credit_score
        approved_amount = request.POST.get('approved_amount')
        amount_to_disburse = get_amount_to_disburse(loan)

        if member_score >= 5 and guarantors_score >= 7:

            if is_sufficient_collateral(loan):
                if loan.status == 'pending':
                    #update loan details
                    loan.approved_amount = approved_amount
                    loan.disbursed_amount = amount_to_disburse
                    loan.approved_date = today
                    loan.approved_by = companystaff
                    loan.status = 'approved'

                    #update borrower details
                    borrower.status = 'active'
                    borrower.save()
                    loan.save()
                    messages.success(request,'The loan was approved successfully!')
                    return redirect('view-loan', loan.id)
            else:
                messages.error(request, 'The collateral value is too low!')
                return redirect('view-loan', loan.id)
        else:
            messages.error(request, 'Approval failed!, borrower/guarantor flagged')
            return redirect('view-loan', loan.id)

    return redirect('view-loan', loan.id)
#approve logic ends

#approve loan logic starts here
#@role_required
def rejectLoan(request,pk):
    if request.method == 'POST':

        if request.user.is_authenticated and request.user.is_active:
            try:
                companystaff = CompanyStaff.objects.get(username=request.user.username)
                company = companystaff.company
            except CompanyStaff.DoesNotExist:
                company = None
        else:
            company = None

        loan = Loan.objects.get(id=pk, company=company)
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
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
    
    form = LoanForm(request.POST, company=company) #instiated the two kwargs to be able to access them on the forms.py
    loans = Loan.objects.filter(company=company)

    context = {'loans': loans, 'form':form}
    return render(request, 'loan/loans-list.html', context)

# list Loan  view ends


# detailview Loan  view starts 
def viewLoan(request, pk):
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
    loan = Loan.objects.get(id=pk, company=company)
    borrower = loan.member
    
    loan_notes = loan.note_set.all().order_by('-created')
    guarantors = Guarantor.objects.filter(loan=loan) #here loan=loan mean loan_obj=loan loan_obj in guarantor model and form
    collaterals = Collateral.objects.filter(loan=loan)
    repayments = Repayment.objects.filter(loan_id=loan)
    statements = MpesaStatement.objects.filter(loan_id=loan)

    form = GuarantorForm(request.POST,company=company, borrower=borrower)
    form_collateral = CollateralForm()
    form_repayment = RepaymentForm()
    form_statement = MpesaStatementForm()

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

    if request.method == 'POST' and 'body' in request.POST:
        Note.objects.create(
            company = company,
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
        'statements':statements,
        'form_collateral':form_collateral,
        'form_repayment':form_repayment,
        'form_statement' : form_statement
        }
    return render(request, 'loan/loan-view.html', context)

# detailview Loan  view ends


# delete Loan  view starts
@role_required 
def deleteLoan(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

    loan = Loan.objects.filter(id=pk, company=company)
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

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    form = RepaymentForm(request.POST, company=company) 
    #processing the data
    if request.method == 'POST':
        member_id = request.POST.get('member')
        member = Member.objects.get(pk=member_id, company=company)
        # Get the approved or overdue Loan object associated with the member
        loan = member.loans_as_member.get(status=('approved' or 'overdue'))
        if loan:
            Repayment.objects.create(
                company = company,
                transaction_id= request.POST.get('transaction_id'),
                loan_id = loan,
                member = member,
                amount= request.POST.get('amount'),
                date_paid = request.POST.get('date_paid'),
            )
            
            clear_loan(loan) #clear a loan
            update_member_data(loan) #update member/borrower data
            messages.success(request,'The repayment was added succussesfully!')
            return redirect('repayments')
        else:
            messages.error(request, 'You cannot add a repayment to a cleared or pending loan')
            return redirect('repayments')
    context= {'form':form}
    return render(request,'loan/repayment-create.html', context)
#-- ends --

# list Repayments  view starts 
def listRepayments(request):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    form = RepaymentForm(request.POST, company=company)
    repayments = Repayment.objects.filter(company=company)

    context = {'repayments': repayments, 'form':form}
    return render(request, 'loan/repayment-list.html', context)

# list Repayment  view ends

# delete Repayment  view starts 
def deleteRepayment(request,pk):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

    repayment = Repayment.objects.filter(id=pk, company=company)
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
        
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    repayment = Repayment.objects.get(id=pk, company=company)
    
    if request.method == 'POST':
        form = RepaymentForm(request.POST, instance=repayment, company=company)

        member_id = request.POST.get('member')
        member = Member.objects.get(pk=member_id, company=company)

        loan = member.loans_as_member.get(status=('approved' or 'overdue'))

        if form.is_valid():
            repayment= form.save(commit=False)
            repayment.loan_id = loan
            repayment.company = company
            repayment.save()

            clear_loan(loan) #clear a loan
            update_member_data(loan) #update member/borrower data
            messages.success(request,'The repayment was edited succussesfully!')
            return redirect('repayments')
        else:
            messages.error(request, 'Fill the form as required')
    # prepopulate the form with existing data
    form = RepaymentForm(instance=repayment, company=company)
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

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)
    borrower = loan.member

    guarantor_id = request.POST.get('name')
    guarantor = Member.objects.get(id=guarantor_id)
    
    if request.method == 'POST':
        form = GuarantorForm(request.POST, company=company, borrower=borrower) 

        Guarantor.objects.create(
            company = company,
            loan = loan,
            name = guarantor,
            amount = request.POST.get('amount')
        )
        messages.success(request, 'Guarantor added successfully.')
        return redirect('view-loan', pk=loan.id)
       
    context= {'form':form, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
#dd guarontor view ends   


# delete guarantor  view starts 
def removeGuarantor(request, pk, guarantor_id):
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)
    guarantor = get_object_or_404(Guarantor, id=guarantor_id, loan=loan)

    if request.method == 'POST':
        guarantor.delete()
        messages.success(request, 'Guarantor deleted successfully.')
        return redirect('view-loan', pk=loan.id)

    context = {'obj':guarantor, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
# delete guarantor  ends 

#add guarontor view starts
def addCollateral(request, pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)

    form = CollateralForm(request.POST)
    #processing the data
    if request.method == 'POST':
        Collateral.objects.create(
            company = company,
            loan = loan,
            name = request.POST.get('name'),
            type = request.POST.get('type'),
            estimated_value = request.POST.get('estimated_value'), 
            serial_number = request.POST.get('serial_number')
        )
        messages.success(request, 'Collateral added successfully.')
        return redirect('view-loan', pk=loan.id)
 
    context= {'form':form}
    return render(request,'loan/loan-view.html', context)
#dd guarontor view ends   

# delete collateral  view starts 
def removeCollateral(request, pk, collateral_id):
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)
    collateral = get_object_or_404(Collateral, id=collateral_id, loan=loan)

    if request.method == 'POST':
        collateral.delete()
        messages.success(request, 'Collateral deleted successfully.')
        return redirect('view-loan', pk=loan.id)

    context = {'obj':collateral, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
# delete collateral  ends 


#add guarontor view starts
def editCollateral(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    collateral = get_object_or_404(Collateral, id=pk, company=company)

    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = Loan.objects.get(pk=loan_id)

        # Get the URL pattern for the 'view-loan' view
        url = reverse('view-loan', args=[loan_id])

        # Append the anchor to the end of the URL
        url_with_anchor = f'{url}#tabItem18'

        collateral.company = company
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
        form = CollateralForm(initial=form_data, company=company)
        context= {'form':form}
        return render(request,'loan/loan-view.html', context)
 
#edit collateral view ends  

#add repayment on a loanview view starts
def addRepayment(request, pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)

    member = loan.member #retrieving the loan borrower
    form = RepaymentForm(request.POST, company=company)
    #processing the data
    if request.method == 'POST':
        Repayment.objects.create(
            company = company,
            transaction_id = request.POST.get('transaction_id'),
            loan = loan,
            member = member,
            amount = request.POST.get('amount'),
            date_paid = request.POST.get('date_paid')
        )
        clear_loan(loan) #clear a loan
        update_member_data(loan) #update member/borrower data
        messages.success(request, 'Repayment added successfully.')
        return redirect('view-loan', pk=loan.id)
 
    context= {'form':form, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
#add repayment on a loanview view ends 
  
#add statement view starts
def addStatement(request, pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)
    borrower = loan.member
    form = MpesaStatementForm(request.POST) 

    if request.method == 'POST':
        form = MpesaStatementForm(request.POST) 

        MpesaStatement.objects.create(
            company = company,
            loan = loan,
            owner = borrower, 
            code = request.POST.get('code'),
            statements = request.FILES.get('statements')
        )
        messages.success(request, 'Statement loaded added successfully.')
        return redirect('view-loan', pk=loan.id)
       
    context= {'form':form, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
# view ends   

#analyse statement view starts
def analyseStatement(request, pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    loan = get_object_or_404(Loan, id=pk, company=company)
    statement_id = request.POST.get('statement_id')
    statement = get_object_or_404(MpesaStatement, id=statement_id, company=company)
    
    file_path= str(statement.statements)
    file_path = os.path.join(settings.BASE_DIR, 'static', 'media', file_path) #absolute path for the file

    file_password= statement.code
    loan_table = get_loans_table(file_path, file_password)
       
    context= {'loan':loan,'file_path':file_path, 'loan_table':loan_table}
    return render(request,'loan/analysis.html', context)
#dd  view ends  