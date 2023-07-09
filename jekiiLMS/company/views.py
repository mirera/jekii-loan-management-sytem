from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Organization, Package
from .forms import OrganizationForm, PackageForm, SmsForm, MpesaSettingForm, EmailSettingForm, SystemSettingForm
from user.models import CompanyStaff
from branch.models import Branch
from member.models import Member
from company.models import SmsSetting, MpesaSetting, EmailSetting, SystemSetting, SecuritySetting
from jekiiLMS.cred_process import encrypt_secret
from jekiiLMS.decorators import permission_required
from jekiiLMS.format_inputs import format_phone_number, deformat_phone_no

#-- update organization details upon sign up view --
@login_required(login_url='login')
@permission_required('company.change_organization') 
def updateOrganization(request, pk):
    organization = Organization.objects.get(id=pk)
    admins = CompanyStaff.objects.filter(company=organization, user_type='admin')

    #check if sms_setting instance exist, if none, create
    try:
        sms_setting = SmsSetting.objects.get(company=organization)
    except SmsSetting.DoesNotExist:
        # create new SmsSetting object for the organization
        sms_setting = SmsSetting.objects.create(company=organization)

    #if mpesa_setting obj none, create
    try:
        mpesa_setting = MpesaSetting.objects.get(company=organization)
    except MpesaSetting.DoesNotExist:
        # create 
        mpesa_setting = MpesaSetting.objects.create(company=organization)
    
    #if email_setting obj none, create
    try:
        email_setting = EmailSetting.objects.get(company=organization)
    except EmailSetting.DoesNotExist:
        # create 
        email_setting = EmailSetting.objects.create(company=organization)

    #if preference obj none, create
    
    try:
        preferences = SystemSetting.objects.get(company=organization)
    except SystemSetting.DoesNotExist:
        # create 
        preferences = SystemSetting.objects.create(company=organization)

    try:
        security_setting = SecuritySetting.objects.get(company=organization)
    except SecuritySetting.DoesNotExist:
        # create 
        security_setting = SecuritySetting.objects.create(company=organization)

    old_phone_code = organization.phone_code

    if request.method == 'POST':
        phone_no = request.POST.get('phone_no') 
        phone_code = request.POST.get('phone_code') 
        formatted_phone = format_phone_number(phone_no, phone_code)
        #update company details
        organization.name = request.POST.get('name')
        organization.email = request.POST.get('email')
        organization.country = request.POST.get('country')
        organization.phone_no = formatted_phone
        organization.email = request.POST.get('email')
        organization.logo = request.FILES.get('logo')
        organization.address = request.POST.get('address')
        organization.currency = request.POST.get('currency')
        organization.timezone = request.POST.get('timezone')
        organization.phone_code = request.POST.get('phone_code')
        organization.save()

        #update db phone enties with new phonecode
        branches = Branch.objects.filter(company=organization)
        for branch in branches:
            deformated_phone = deformat_phone_no(branch.phone, old_phone_code)
            branch.phone = format_phone_number(deformated_phone, phone_code)
            branch.save()
        
        members = Member.objects.filter(company=organization)
        for member in members:
            deformated_phone = deformat_phone_no(member.phone_no, old_phone_code)
            member.phone_no = format_phone_number(deformated_phone, phone_code)
            member.save()
        
        staffs = CompanyStaff.objects.filter(company=organization)
        for staff in staffs:
            deformated_phone = deformat_phone_no(staff.phone_no, old_phone_code)
            staff.phone_no = format_phone_number(deformated_phone, phone_code)
            staff.save()
        
        messages.success(request, 'settings updated successfully')
        return redirect('update-organization', organization.id)
    else:
        # prepopulate the form with existing data
        
        #deformat phone number when displying on form
        deheaded_phone = deformat_phone_no(organization.phone_no, organization.phone_code)
        form_data = {
            'name': organization.name,
            'email': organization.email,
            'country': organization.country,
            'phone_no': deheaded_phone, 
            'email': organization.email,
            'logo': organization.logo, 
            'address': organization.address,
            'currency': organization.currency,
            'timezone': organization.timezone,
            'phone_code': organization.phone_code,
        }
        # prefill the sms form 
        form_data_sms = {
            'sender_id': sms_setting.sender_id,
            'api_token': sms_setting.api_token
        }
        # prefill the mpesa form 
        form_data_mpesa = {
            'shortcode': mpesa_setting.shortcode,
            'app_consumer_key': mpesa_setting.app_consumer_key,
            'app_consumer_secret': mpesa_setting.app_consumer_secret,
            'online_passkey': mpesa_setting.online_passkey,
            'username': mpesa_setting.username
        }
        # prefill the email form 
        form_data_email = {
            'from_name': email_setting.from_name,
            'from_email': email_setting.from_email,
            'smtp_host': email_setting.smtp_host,
            'encryption': email_setting.encryption,
            'smtp_port': email_setting.smtp_port,
            'smtp_username': email_setting.smtp_username,
            'smtp_password': email_setting.smtp_password
        }
        # prefill the system preference form 
        form_data_preferences = {
            'is_auto_disburse': preferences.is_auto_disburse,
            'is_send_sms': preferences.is_send_sms,
            'is_send_email': preferences.is_send_email
        }
        form_preferences = SystemSettingForm(initial=form_data_preferences)
        form_email = EmailSettingForm(initial=form_data_email)
        form_mpesa = MpesaSettingForm(initial=form_data_mpesa)
        form_sms = SmsForm(initial=form_data_sms)
        form = OrganizationForm(initial=form_data)
        context = {
            'form':form,
            'form_sms':form_sms,
            'form_mpesa':form_mpesa,
            'form_email':form_email,
            'form_preferences':form_preferences,
            'organization':organization,
            'admins':admins,
            'security_setting':security_setting
        }
       
    return render(request,'company/update-company.html', context)

# -- view to create package
@login_required(login_url='login')
@permission_required('company.add_package')
def createPackage(request):
    form = PackageForm()
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.save()
            messages.success(request, 'Package created successfully')
            return redirect('packages')
        else:
            messages.error(request, 'Form validation failed! Try again.')
    context = {'form':form}        
    return render(request,'company/packages.html', context)
# -- ends

# -- view to list all packages
@login_required(login_url='login')
def listPackages(request):
    packages = Package.objects.all()
    form = PackageForm()
    context = {'packages':packages, 
                'form':form,
            }        
    return render(request,'company/packages.html', context)
# -- ends

# -- view to list all comapnies
@login_required(login_url='login')
@permission_required('company.view_organization')
def listCompanies(request):
    companies = Organization.objects.all()
    form = OrganizationForm()
    context = {'companies':companies, 
                'form':form,
            }        
    return render(request,'company/companies.html', context)
# -- ends

# -- view to add sms setting
@login_required(login_url='login')
#@permission_required('company.change_smssetting')
def updateSms(request, pk):
    organization = Organization.objects.get(id=pk)
    sms_setting = SmsSetting.objects.get(company=organization)
    form_sms = SmsForm()

    if request.method == 'POST':
        #raw api_token
        raw_token = request.POST.get('api_token')
        #encrypt api_token 
        encrypted_token = encrypt_secret(raw_token)

        sms_setting.company = organization
        sms_setting.sender_id = request.POST.get('sender_id')
        sms_setting.api_token = encrypted_token
        sms_setting.save()

        messages.success(request, 'SMS gateway credentials updated successfully.')
        return redirect('update-organization', organization.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'sender_id': sms_setting.sender_id,
            'api_token': sms_setting.api_token
        }
        form_sms = SmsForm(initial=form_data)
 
    context = {
            'form_sms':form_sms
        }
    return render(request,'company/update-company.html', context)
# -- ends 

# -- view to add mpesa setting
@login_required(login_url='login')
#@permission_required('company.change_mpesasetting')
def updateMpesa(request, pk):
    organization = Organization.objects.get(id=pk)
    mpesa_setting = MpesaSetting.objects.get(company=organization)
    form_mpesa = MpesaSettingForm()

    if request.method == 'POST':
        #raw creds
        raw_app_consumer_key = request.POST.get('app_consumer_key')
        raw_app_consumer_secret = request.POST.get('app_consumer_secret')
        raw_online_passkey = request.POST.get('online_passkey')

        #encrypt api_token 
        encrypted_app_consumer_key = encrypt_secret(raw_app_consumer_key)
        encrypted_app_consumer_secret = encrypt_secret(raw_app_consumer_secret)
        encrypted_online_passkey = encrypt_secret(raw_online_passkey)

        mpesa_setting.company = organization
        mpesa_setting.shortcode = request.POST.get('shortcode')
        mpesa_setting.app_consumer_key = encrypted_app_consumer_key
        mpesa_setting.app_consumer_secret = encrypted_app_consumer_secret
        mpesa_setting.online_passkey = encrypted_online_passkey
        mpesa_setting.username = request.POST.get('username')
        mpesa_setting.save()

        messages.success(request, 'Mpesa gateway credentials updated successfully.')
        return redirect('update-organization', organization.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'sender_id': mpesa_setting.shortcode,
            'api_token': mpesa_setting.app_consumer_key,
            'api_token': mpesa_setting.app_consumer_secret,
            'api_token': mpesa_setting.online_passkey,
            'api_token': mpesa_setting.username,
        }
        form_mpesa = MpesaSettingForm(initial=form_data)
 
    context = {
            'form_mpesa':form_mpesa
        }
    return render(request,'company/update-company.html', context)
# -- ends

# -- view to add mpesa setting
@login_required(login_url='login')
#@permission_required('company.change_emailsetting')
def updateEmail(request, pk):
    organization = Organization.objects.get(id=pk)
    email_setting = EmailSetting.objects.get(company=organization)
    form_email = EmailSettingForm()

    if request.method == 'POST':
        #raw creds
        raw_smtp_password = request.POST.get('smtp_password')

        #encrypt password 
        encrypted_smtp_password= encrypt_secret(raw_smtp_password)

        email_setting.company = organization
        email_setting.from_name = request.POST.get('from_name')
        email_setting.from_email = request.POST.get('from_email')
        email_setting.smtp_host = request.POST.get('smtp_host')
        email_setting.encryption = request.POST.get('smtp_host')
        email_setting.smtp_port = request.POST.get('smtp_port')
        email_setting.smtp_username = request.POST.get('smtp_username')
        email_setting.smtp_password = encrypted_smtp_password
        email_setting.save()

        messages.success(request, 'Email credentials updated successfully. Send Test Email to confirm if they work as expected.')
        return redirect('update-organization', organization.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'from_name': email_setting.from_name,
            'from_email': email_setting.from_email,
            'smtp_host': email_setting.smtp_host,
            'encryption': email_setting.encryption,
            'smtp_port': email_setting.smtp_port,
            'smtp_username': email_setting.smtp_username,
            'smtp_password': email_setting.smtp_password,
        }
        form_email = EmailSettingForm(initial=form_data)
 
    context = {
            'form_email':form_email
        }
    return render(request,'company/update-company.html', context)
# -- ends

# -- view to send test email
@login_required(login_url='login')
def sendTestEmail(request, pk):
    organization = Organization.objects.get(id=pk)
    email_setting = EmailSetting.objects.get(company=organization)
    if request.method == 'POST':
        #from form
        email = request.POST.get('email')
        mail_message = request.POST.get('message')

        #send mail .
        context = {'mail_message':mail_message}
        from_name_email = f'{email_setting.from_name} <{email_setting.from_email}>' 
        template = render_to_string('company/test-email.html', context)

        e_mail = EmailMessage(
            'Email Successfully Sent',
            template,
            from_name_email,
            [email],
            reply_to=[email_setting.from_email],
        )
        try:
            e_mail.send(fail_silently=False)
        except:
            messages.error(request, 'Failed to send email')
            return redirect('update-organization', organization.id)
        else:
            messages.success(request, 'Email sent successfully')
            return redirect('update-organization', organization.id)
    return redirect('update-organization', organization.id)
# -- ends

# update prefenrences view
@login_required(login_url='login')
def updatePreferences(request, pk):
    organization = Organization.objects.get(id=pk)
    preferences, created = SystemSetting.objects.get_or_create(company=organization)

    if request.method == 'POST':
        form_preferences = SystemSettingForm(request.POST, instance=preferences)
        if form_preferences.is_valid():
            is_auto_disburse = request.POST.get('is_auto_disburse') == 'on'
            is_send_sms = request.POST.get('is_send_sms') == 'on' 
            is_send_email = request.POST.get('is_send_email') == 'on' 
            preferences = form_preferences.save(commit=False)
            preferences.company = organization
            preferences.is_auto_disburse = is_auto_disburse
            preferences.is_send_sms = is_send_sms
            preferences.is_send_email = is_send_email
            preferences.save()
        messages.success(request, 'System preferences updated successfully.')
        return redirect('update-organization', organization.id)
    else:

        # prepopulate the form with existing data
        form_data = {
            'is_auto_disburse': preferences.is_auto_disburse,
            'is_send_sms': preferences.is_send_sms,
            'is_send_email': preferences.is_send_email
        }
        form_preferences = SystemSettingForm(initial=form_data)
 
    context = {
            'form_preferences':form_preferences,
        }
    
    return render(request,'company/update-company.html', context) 
# --ends

#security setting views
#disable two factor auth
@login_required(login_url='login')
def disable_2fa(request, pk):
    organization = Organization.objects.get(id=pk)
    security_setting, created = SecuritySetting.objects.get_or_create(company=organization)
    security_setting.two_fa_auth = False
    security_setting.save()
    return redirect('update-organization', organization.id)

#enable two factor auth
@login_required(login_url='login')
def enable_2fa(request, pk):
    organization = Organization.objects.get(id=pk)
    security_setting, created = SecuritySetting.objects.get_or_create(company=organization)
    if security_setting.two_fa_auth == False:
        security_setting.two_fa_auth = True
        security_setting.save()
    return redirect('update-organization', organization.id)

