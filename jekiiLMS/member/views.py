from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required 
from .models import Member, Branch
from .forms import MemberForm
from user.models import CompanyStaff
from loan.models import Loan
from company.models import SmsSetting, SystemSetting
from jekiiLMS.decorators import permission_required
from jekiiLMS.tasks import send_email_task, send_sms_task
from jekiiLMS.utils import get_user_company, delete_member
from jekiiLMS.format_inputs import format_phone_number, deformat_phone_no, user_local_time,to_utc


#create member view starts
@login_required(login_url='login')
@permission_required('member.add_member')
def createMember(request):
    #filter the Branch queryset to include only branches that belong to the logged in company 
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

    form = MemberForm(request.POST, company=company) #instiated the two kwargs to be able to access them on the forms.py

    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(id=branch_id)
        phone_no = request.POST.get('phone_no')
        formated_phone_no = format_phone_number(phone_no, company.phone_code)

        date_joined_str = request.POST.get('date_joined')
        date_joined = datetime.strptime(date_joined_str, '%Y-%m-%d')  # Convert to datetime 
        utcz_datetime = to_utc(company.timezone, date_joined)
        
        member = Member.objects.create(
            company = company,
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            id_no= request.POST.get('id_no'),
            phone_no = formated_phone_no,
            branch = branch,
            email= request.POST.get('email'),
            date_joined= utcz_datetime,
            business_name = request.POST.get('business_name'),
            industry = request.POST.get('industry'),
            address = request.POST.get('address'),
            passport_photo=request.FILES.get('passport_photo')
        )
        preferences = SystemSetting.objects.get(company=company)
        sms_setting = SmsSetting.objects.get(company=member.company)
        sms_message = 'Some user customer SMS template'
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token         
        if sender_id is not None and token is not None and preferences.on_joining:
            send_sms_task.delay(
                sender_id,
                token,
                member.phone_no, 
                message=sms_message,
            )

        messages.success(request, 'Member added successfully.')
        return redirect('members')

    context= {'form':form}
    return render(request,'member/create-member.html', context)
#create member view ends

# list member view starts 
@login_required(login_url='login')
@permission_required('member.view_member')
def listMembers(request):
    #filter the Branch queryset to include only branches that belong to the logged in company 
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    
    form = MemberForm(request.POST, company=company) #instiated the two kwargs to be able to access them on the forms.py
    #company = request.user.organization
    members = Member.objects.filter(company=company).order_by('-date_joined')

    context = {'members': members, 'form':form}
    return render(request, 'member/members-list.html', context)
# list member view ends

# list blacklisted member  
@login_required(login_url='login')
@permission_required('member.view_member')
def blacklisted_members(request):
    company = get_user_company(request)
    form = MemberForm(request.POST, company=company) 
    members = Member.objects.filter(company=company, credit_score__lt=4).order_by('-date_joined')
    context = {
        'members': members,
        'form':form, 
        }
    return render(request, 'member/backlisted-members.html', context)
# list member view ends

# view member view starts 
@login_required(login_url='login')
@permission_required('member.view_member')
def viewMember(request, pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

    member = Member.objects.get(id=pk, company=company)
    print(member)
    context = {'member': member}
    return render(request, 'member/member-view.html', context) 
# view member view ends

# delete member view starts
@login_required(login_url='login')
@permission_required('member.delete_member')
def deleteMember(request,pk):
    #member = Member.objects.get(id=pk)
    member = get_object_or_404(Member, id=pk)

    if request.method == 'POST':
        member.delete()
        return redirect('members')

    context = {'member':member}
    return render(request,'member/delete-member.html', context)
# delete member ends 

#edit member view starts
@login_required(login_url='login')
@permission_required('member.change_member')
def editMember(request,pk):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

    member = Member.objects.get(id=pk, company=company)

    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        # Get the selected branch id from the form
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(pk=branch_id)

        date_joined_str = request.POST.get('date_joined')
        date_joined = datetime.strptime(date_joined_str, '%Y-%m-%d')  # Convert to datetime 
        utcz_datetime = to_utc(company.timezone, date_joined)

        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.id_no = request.POST.get('id_no')
        member.phone_no = format_phone_number(phone_no, company.phone_code)
        member.email = request.POST.get('email')
        member.date_joined = utcz_datetime
        member.branch = branch
        member.business_name = request.POST.get('business_name')
        member.industry = request.POST.get('industry')
        member.address = request.POST.get('address')
        member.credit_score = request.POST.get('credit_score')
        member.passport_photo = request.FILES.get('passport_photo')

        

        member.save()
        messages.success(request, 'Member edited successfully')
        return redirect('members')
    else:
        # prepopulate the form with existing data
        form_data = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'id_no': member.id_no,
            'phone_no': deformat_phone_no(member.phone_no, member.company.phone_code),
            'email': member.email,
            'branch': member.branch,
            'date_joined': user_local_time(company.timezone, member.date_joined),
            'business_name': member.business_name,
            'industry': member.industry,
            'address': member.address,
            'credit_score': member.credit_score,
            'passport_photo': member.passport_photo,
        }

        form = MemberForm(initial=form_data, company=company )
        return render(request,'member/edit-member.html',{'form':form})
#edit member view ends    

# sms member
@login_required(login_url='login')
def sms_member(request, pk):
    if request.method == 'POST':
        #get the member to sms
        try:
            member = Member.objects.get(id=pk)
        except:
            member = None
        #get message body
        sms_message = request.POST.get('sms_message')
        print(f'This is the selected member hould be mirera:{member}')
        #send sms
        sms_setting = SmsSetting.objects.get(company=member.company)
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token         
        if sender_id is not None and token is not None:
            send_sms_task.delay(
                sender_id,
                token,
                member.phone_no, 
                message=sms_message,
            )
            messages.success(request, f'Message successful sent to {member.first_name}.')
    return redirect('members')
 
 #member bulky actions - in the member table
@login_required(login_url='login')
def members_bulky_action(request):
    company=get_user_company(request)
    if request.method == 'POST':
        # Retrieve the selected option from the form data
        bulk_action = request.POST.get('bulk-action')
        selected_ids = request.POST.getlist('selected_ids')
        selected_members = []
        for member_id in selected_ids:
            member = Member.objects.get(id=member_id)
            selected_members.append(member)
        if bulk_action == 'sms':
            #get message from POST Request
            sms_message_raw = request.POST.get('sms_message')
            system_preferences = SystemSetting.objects.get(company=company)

            for member in selected_members:
                loan = Loan.objects.filter(company=company, member=member).order_by('-application_date').first()
                if system_preferences.is_send_sms:
                    #available tags 
                    first_name = member.first_name
                    last_name = member.last_name
                    organization_name = company.name
                    currency = company.currency
                    account_no = company.account_no
                    paybill_no = company.paybill_no
                    #handling a case where a loan is pending or rejected and it has no the below
                    if loan.status in ['pending', 'rejected']:
                        due_amount = 0
                        loan_balance = 0
                        final_date = "na"
                    else:
                        due_amount = loan.due_amount
                        final_date = loan.final_due_date
                        loan_balance = loan.loan_balance()
                    

                    #format raw message template 
                    message_raw = sms_message_raw
                    message = message_raw.format(
                        first_name=first_name, 
                        last_name=last_name, 
                        organization_name=organization_name, 
                        currency=currency,
                        due_amount=due_amount,
                        loan_balance=loan_balance,
                        final_date=final_date,
                        account_no=account_no,
                        paybill_no=paybill_no,
                    )
                    #send sms
                    sms_setting = SmsSetting.objects.get(company=member.company) 
                    sender_id = sms_setting.sender_id
                    token = sms_setting.api_token 
                    preferences = SystemSetting.objects.get(company=member.company)
                    if preferences.is_send_sms and sender_id is not None and token is not None:
                        send_sms_task.delay(
                            sender_id,
                            token,
                            member.phone_no, 
                            message,
                        )

            messages.success(request, 'Messages sent.')
            return redirect('members')

        elif bulk_action == 'delete':
            #delete users
            delete_member(uid=member.id)
            messages.success(request, 'Selected members deleted.')
            return redirect('members')

    return redirect('members')



    