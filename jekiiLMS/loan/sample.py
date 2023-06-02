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
from django.utils import timezone
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jekiiLMS.decorators import permission_required
from .models import LoanProduct, Loan, Note, Repayment, Guarantor, Collateral, MpesaStatement
from .forms import LoanProductForm, LoanForm, RepaymentForm, GuarantorForm, CollateralForm, MpesaStatementForm
from member.models import Member
from user.models import RecentActivity, Notification
from user.models import CompanyStaff
from company.models import Organization, SmsSetting, MpesaSetting, EmailSetting, SystemSetting
from jekiiLMS.process_loan import is_sufficient_collateral, get_amount_to_disburse, clear_loan, update_member_data, write_loan_off, roll_over
from jekiiLMS.mpesa_statement import get_loans_table
from jekiiLMS.loan_math import loan_due_date, save_due_amount, total_interest, installments
from jekiiLMS.sms_messages import send_sms
from jekiiLMS.mpesa_api import disburse_loan
from jekiiLMS.format_inputs import to_utc, user_local_time
from jekiiLMS.utils import get_user_company
from jekiiLMS.tasks import send_email_task, send_sms_task, disburse_loan_task

#approve loan logic starts here
@login_required(login_url='login')
@permission_required('loan.approve_loan')
def approveLoan(request,pk):
    if request.method == 'POST':
        staff = CompanyStaff.objects.get(username=request.user.username)
        company = get_user_company(request)
        loan = Loan.objects.get(id=pk, company=company)
        borrower = loan.member
        guarantors = Guarantor.objects.filter(loan=loan)
        #today = datetime.today().strftime('%Y-%m-%d')
        today = timezone.now() #converted to uct already

        guarantors_score = 0
        for guarantor in guarantors:
            guarantors_score += guarantor.name.credit_score

        member_score = borrower.credit_score
        approved_amount = int(request.POST.get('approved_amount'))
        amount_to_disburse = get_amount_to_disburse(loan, approved_amount)
        due_date = loan_due_date(loan)
        installment = installments(loan.loan_product)

        if member_score >= 5 and guarantors_score >= 7:
            if is_sufficient_collateral(loan):
                if loan.status == 'pending':
                    #update loan details
                    loan.approved_amount = int(approved_amount)
                    loan.disbursed_amount = amount_to_disburse
                    loan.approved_date = today
                    loan.approved_by = staff
                    loan.status = 'approved'
                    loan.due_date = due_date
                    loan.num_installments = installment

                    #update borrower details
                    borrower.status = 'active'
                    borrower.save()
                    loan.save()

                    #send mail arguments.
                    email_setting = EmailSetting.objects.get(company=company)
                    context = {'loan':loan}
                    from_name = email_setting.from_name
                    from_email = email_setting.from_email
                    template_path = 'loan/loan-approved.html'
                    subject = 'Loan Approved'
                    recipient_email = borrower.email
                    replyto_email = company.email

                    #send sms aurguments
                    sms_setting = SmsSetting.objects.get(company=company)
                    sender_id = sms_setting.sender_id
                    token = sms_setting.api_token 
                    date = loan.due_date.date().strftime('%Y-%m-%d')
                    message = f"Dear {borrower.first_name}, Your loan request has been approved and queued for disbursal. The next payment date {date}, amount Ksh{loan.due_amount}. Acc. 5840988 Paybill 522522"  

                    system_setting = SystemSetting.objects.get(company=company)
                    if system_setting.is_auto_disburse:
                        #disburse loan
                        mpesa_setting = MpesaSetting.objects.get(company=company)
                        consumer_key = mpesa_setting.app_consumer_key
                        consumer_secret = mpesa_setting.app_consumer_secret
                        shortcode = mpesa_setting.shortcode
                        username = mpesa_setting.username
                        try:
                            disbursement_response = disburse_loan_task.delay(
                                                        consumer_key,
                                                        consumer_secret, 
                                                        shortcode,
                                                        username, 
                                                        loan
                                                    )

                            if disbursement_response['ResponseCode'] == '0':
                                # call fill due_amount function to fill due_amount & final payment date on the Loan model 
                                save_due_amount(loan)

                                # Create a recent activity entry for loan approval
                                RecentActivity.objects.create(
                                    company = company,
                                    event_type='loan_approval',
                                    details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been approved.'
                                )
                                Notification.objects.create(
                                    company = company,
                                    recipient = loan.loan_officer,
                                    state='info',
                                    message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been approved & disbursed.'
                                )
                                
                                #Enqueue the send_sms_task
                                send_sms_task.delay(
                                    sender_id, 
                                    token, 
                                    borrower.phone_no, 
                                    message
                                )
                                send_email_task.delay(
                                    context, 
                                    template_path, 
                                    from_name, 
                                    from_email, 
                                    subject, 
                                    recipient_email, 
                                    replyto_email
                                )
                                
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
                        # fill due_amount & final payment date on the Loan model 
                        save_due_amount(loan)

                        #Enqueue the send_sms_task and send email tasks
                        send_sms_task.delay(
                            sender_id, 
                            token, 
                            borrower.phone_no, 
                            message
                        )
                        send_email_task.delay(
                            context, 
                            template_path, 
                            from_name, 
                            from_email, 
                            subject, 
                            recipient_email, 
                            replyto_email
                        )

                        # Create a recent activity entry for loan approval
                        RecentActivity.objects.create(
                            company = company,
                            event_type='loan_approval',
                            details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been approved.'
                        )
                        Notification.objects.create(
                            company = company,
                            recipient = loan.loan_officer,
                            state='info',
                            message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been approved waiting for disbursal.'
                        )                        
                        messages.success(request, 'Loan approved, waiting for disbursal!')
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
@permission_required('loan.approve_loan')
def approveLoan(request,pk):
    if request.method == 'POST':
        staff = CompanyStaff.objects.get(username=request.user.username)
        company = get_user_company(request)
        loan = Loan.objects.get(id=pk, company=company)
        borrower = loan.member
        guarantors = Guarantor.objects.filter(loan=loan)
        #today = datetime.today().strftime('%Y-%m-%d')
        today = timezone.now() #converted to uct already

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
        installment = installments(loan.loan_product)

        if member_score >= 5 and guarantors_score >= 7:

            if is_sufficient_collateral(loan):
                if loan.status == 'pending':
                    #update loan details
                    loan.approved_amount = int(approved_amount)
                    loan.disbursed_amount = amount_to_disburse
                    loan.approved_date = today
                    loan.approved_by = staff
                    loan.status = 'approved'
                    loan.due_date = due_date
                    loan.num_installments = installment

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

                            # Create a recent activity entry for loan approval
                            RecentActivity.objects.create(
                                company = company,
                                event_type='loan_approval',
                                details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been approved.'
                            )
                            Notification.objects.create(
                                company = company,
                                recipient = loan.loan_officer,
                                state='info',
                                message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been approved.'
                            )
                            
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