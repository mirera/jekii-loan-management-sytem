from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
import os
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jekiiLMS.decorators import permission_required
from .models import LoanProduct, Loan, Note, Repayment, Guarantor, Collateral, MpesaStatement
from .forms import LoanProductForm, LoanForm, RepaymentForm, GuarantorForm, CollateralForm, MpesaStatementForm
from member.models import Member
from user.models import CompanyStaff
from company.models import Organization, SmsSetting, MpesaSetting, EmailSetting
from jekiiLMS.process_loan import is_sufficient_collateral, get_amount_to_disburse, clear_loan, update_member_data, write_loan_off, roll_over
from jekiiLMS.mpesa_statement import get_loans_table
from jekiiLMS.loan_math import loan_due_date, save_due_amount, num_installments, total_interest, final_date
from jekiiLMS.sms_messages import send_sms
from jekiiLMS.mpesa_api import disburse_loan



#create Loan Product view starts 
@login_required(login_url='login')
@permission_required('loan.add_loanproduct')
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
@login_required(login_url='login')
@permission_required('loan.view_loanproduct') 
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
@login_required(login_url='login')
@permission_required('loan.view_loanproduct') 
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
@login_required(login_url='login')
@permission_required('loan.delete_loanproduct')
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
@login_required(login_url='login')
@permission_required('loan.change_loanproduct')
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
@login_required(login_url='login')
@permission_required('loan.add_loan')
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
@login_required(login_url='login')
@permission_required('loan.change_loan')
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
@login_required(login_url='login')
@permission_required('loan.approve_loan')
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

        #email variables & context
        company_email = company.email
        email = borrower.email

        guarantors_score = 0
        for guarantor in guarantors:
            guarantors_score += guarantor.name.credit_score

        member_score = borrower.credit_score
        approved_amount = int(request.POST.get('approved_amount'))
        amount_to_disburse = get_amount_to_disburse(loan, approved_amount)
        due_date = loan_due_date(loan)
        installments = num_installments(loan)

        if member_score >= 5 and guarantors_score >= 7:

            if is_sufficient_collateral(loan):
                if loan.status == 'pending':
                    #update loan details
                    loan.approved_amount = int(approved_amount)
                    loan.disbursed_amount = amount_to_disburse
                    loan.approved_date = today
                    loan.approved_by = companystaff
                    loan.status = 'approved'
                    loan.due_date = due_date
                    loan.num_installments = installments

                    #update borrower details
                    borrower.status = 'active'
                    borrower.save()
                    loan.save()

                    #disburse loan
                    mpesa_setting = MpesaSetting.objects.get(company=loan.company)
                    consumer_key = mpesa_setting.app_consumer_key
                    consumer_secret = mpesa_setting.app_consumer_secret
                    shortcode = mpesa_setting.shortcode
                    username = mpesa_setting.username
                    try:
                        disbursement_response = disburse_loan(
                            consumer_key, 
                            consumer_secret,
                            shortcode,
                            username,
                            loan
                        )
                        if disbursement_response['ResponseCode'] == '0':
                            # call fill due_amount function to fill due_amount & final payment date on the Loan model 
                            save_due_amount(loan)

                            #send mail and message to borrower.
                            email_setting = EmailSetting.objects.get(company=company)
                            context = {'loan':loan}
                            from_name_email = f'{email_setting.from_name} <{email_setting.from_email}>' 
                            template = render_to_string('loan/loan-approved.html', context)
                            e_mail = EmailMessage(
                                'Loan Approved and Disbursed',
                                template,
                                from_name_email, #'John Doe <john.doe@example.com>'
                                [email],
                                reply_to=[company_email, email_setting.from_email],
                            )
                            e_mail.send(fail_silently=False)

                            #send sms
                            sms_setting = SmsSetting.objects.get(company=company)
                            sender_id = sms_setting.sender_id
                            token = sms_setting.api_token 
                            date = loan.due_date.date().strftime('%Y-%m-%d')
                            message = f"Dear {borrower.first_name}, Your loan request has been approved and disbursed. The next payment date {date}, amount Ksh{loan.due_amount}. Acc. 5840988 Paybill 522522"
                            send_sms(
                                sender_id,
                                token,
                                borrower.phone_no,
                                message)

                            messages.success(request, 'Loan approved & disbursed successfully!')
                            return redirect('view-loan', loan.id)
                        else:
                            #undo loan and member status and save
                            loan.status = 'pending'
                            borrower.status = 'inactive'
                            borrower.save()
                            loan.save()
                            messages.error(request, 'Loan disbursement failed!')
                            return redirect('view-loan', loan.id)
                    except Exception as errors:
                        messages.error(request, f'Loan disbursement failed! {str(errors)}')
                        return redirect('view-loan', loan.id)
            else:
                messages.error(request, 'The collateral value is too low!')
                return redirect('view-loan', loan.id)
        else:
            messages.error(request, 'Approval failed!, guarantor or borrower credit score not enough')
            return redirect('view-loan', loan.id)

    return redirect('view-loan', loan.id)
#approve logic ends

#approve loan logic starts here
@login_required(login_url='login')
@permission_required('loan.reject_loan')
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
        borrower = loan.member

        #email variables
        company_name = company.name
        company_email =company.email
        email = loan.member.email

        url = reverse('view-loan', args=[pk])
        url_with_anchor = f'{url}'
        if loan.status == 'pending':
            loan.status = 'rejected'
            loan.save()

            #send mail and message to borrower.
            email_setting = EmailSetting.objects.get(company=company)
            context = {'loan':loan}
            from_name_email = f'{email_setting.from_name} <{email_setting.from_email}>' 
            template = render_to_string('loan/loan-rejected.html', context)
            e_mail = EmailMessage(
                'Loan Rejected',
                template,
                from_name_email, #'John Doe <john.doe@example.com>'
                [email],
                reply_to=[company_email, email_setting.from_email],
            )
            e_mail.send(fail_silently=False)

            #send sms
            sms_setting = SmsSetting.objects.get(company=company)
            sender_id = sms_setting.sender_id
            token = sms_setting.api_token 
            message = f"Dear {borrower.first_name}, we regret to inform you that we are unable to approve your loan request at this time."
            send_sms(
                sender_id,
                token,
                borrower.phone_no,
                message)

            messages.info(request,'The loan was rejected succussesfully!')
            return redirect(url_with_anchor)
    return render(request,'loan/loans-list.html')
#approve logic ends

# list Loan  view starts 
@login_required(login_url='login')
@permission_required('loan.view_loan')
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
@login_required(login_url='login')
@permission_required('loan.view_loan')
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
@login_required(login_url='login')
@permission_required('loan.delete_loan')
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
@login_required(login_url='login')
@permission_required('loan.add_repayment')
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
@login_required(login_url='login')
@permission_required('loan.view_repayment')
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
@login_required(login_url='login')
@permission_required('loan.delete_repayment')
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
@login_required(login_url='login')
@permission_required('loan.change_repayment')
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
@login_required(login_url='login')
def loan_calculator(request):
    form =LoanForm()
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
            "table_data": table_data,
            'form':form
        }

        return render(request, "loan/loan-calculator.html", context)

    context = {
        "loanproducts": LoanProduct.objects.all(),
        "table_data": []
    }
    return render(request, "loan/loan-calculator.html", context)
#loan cacl view ends

#add guarontor view starts
@login_required(login_url='login')
@permission_required('loan.add_guarantor')
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
@login_required(login_url='login')
@permission_required('loan.delete_guarantor')
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
@login_required(login_url='login')
@permission_required('loan.add_collateral')
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
@login_required(login_url='login')
@permission_required('loan.delete_collateral')
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
@login_required(login_url='login')
@permission_required('loan.change_collateral')
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
@login_required(login_url='login')
@permission_required('loan.add_repayment')
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
        repayment = Repayment.objects.create(
            company = company,
            transaction_id = request.POST.get('transaction_id'),
            loan_id = loan,
            member = member,
            amount = request.POST.get('amount'),
            date_paid = request.POST.get('date_paid')
        )
        if loan.status == 'written off':
            loan.write_off_expense = loan.write_off_expense - repayment.amount
            loan.save()
        clear_loan(loan) #clear a loan
        update_member_data(loan) #update member/borrower data
        messages.success(request, 'Repayment added successfully.')
        return redirect('view-loan', pk=loan.id)
 
    context= {'form':form, 'loan':loan}
    return render(request,'loan/loan-view.html', context)
#add repayment on a loanview view ends 
  
#add statement view starts
@login_required(login_url='login')
@permission_required('loan.add_mpesastatement')
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
@login_required(login_url='login')
@permission_required('loan.view_loan')
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

# -- api b2c result url 
@login_required(login_url='login')
@csrf_exempt
def b2c_result(request):
    if request.method == 'POST':
        #parse the data display or store on database
        response_data = json.loads(request.body)
        transaction_reference = response_data.get('TransactionReference')
        result_code = response_data.get('ResultCode')
        result_description = response_data.get('ResultDesc')
        # Process the response data and update your database or send a notification to the user
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
# -- ends 

# -- api b2c timeout url 
@login_required(login_url='login')
@csrf_exempt
def b2c_timeout(request):
    if request.method == 'POST':
        response_data = json.loads(request.body)
        transaction_reference = response_data.get('TransactionReference')
        # Process the response data and update your database or send a notification to the user
        messages.error(request, 'The request timeout. Try again!')
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
# -- ends 

# -- repayments callback
@login_required(login_url='login')
@csrf_exempt
def repayment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('TransID')
        phone_no = data.get('MSISDN')
        amount = data.get('TransAmount')
        transaction_time = data.get('TransTime')
        mpesa_shortcode = data.get('shortcode') 

        #get the company receiving repayment
        company = Organization.objects.get(shortcode=mpesa_shortcode)

        #get the member making repayment
        member = Member.objects.get(phone_no=phone_no) 

        #get the loan
        loan = Loan.objects.get(member=member, status__in=['approved','overdue'])

        # Convert transaction_time to datetime object
        transaction_datetime = datetime.strptime(transaction_time, '%Y%m%d%H%M%S') #comsider checking this

        # Create a new Repayment object
        repayment = Repayment.objects.create(
            company = company,
            transaction_id=transaction_id,
            amount=amount,
            member = member,
            loan_id = loan,
            date_paid=transaction_datetime,
        )
        clear_loan(loan) #clear a loan
        update_member_data(loan) #update member/borrower data
        # Return a success response
        return HttpResponse(status=200)

    else:
        # Return an error response if the request method is not POST
        return HttpResponse(status=405)
# -- ends

# -- write off a loan view
@login_required(login_url='login')
@permission_required('loan.write_off_loan')
def writeOff(request, pk):
    loan = Loan.objects.get(id=pk)
    write_loan_off(loan)

    messages.success(request, f'{loan.member} loan has been written off. The loan can still receive repayments')
    return redirect('view-loan', loan.id)
# -- ends

# -- roll over loan view
@login_required(login_url='login')
@permission_required('loan.rollover_loan')
def rollOver(request, pk):
    loan = Loan.objects.get(id=pk)
    borrower = loan.member
    repayments = loan.repayments.all()
    total_repayments = repayments.aggregate(Sum('amount'))['amount__sum'] or 0
    if total_repayments >= total_interest(loan): 
        new_loan = roll_over(loan)
        #send sms
        date = new_loan.due_date.date().strftime('%Y-%m-%d')
        sms_setting = SmsSetting.objects.get(company=loan.company)
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token
        message = f"Dear {borrower.first_name}, Your loan roll over request has been approved. The next payment date {date}, amount Ksh{new_loan.due_amount}. Acc. 5840988 Paybill 522522"
        send_sms(
            sender_id,
            token,
            borrower.phone_no, 
            message
        )

        messages.success(request, f'{loan.member} loan has been rolled over')
        return redirect('view-loan', new_loan.id) #should be a new loan.id
    else:
        messages.error(request, f'{loan.member} loan can not be rolled over. Member should clear loan interest first, then try again.')
        return redirect('view-loan', loan.id) #should be a new loan.id
# -- ends
