from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Organization, Package
from .forms import OrganizationForm, PackageForm, SmsForm, MpesaSettingForm
from user.models import CompanyStaff
from company.models import SmsSetting, MpesaSetting
from jekiiLMS.cred_process import encrypt_secret

#-- update organization details upon sign up view --
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

    
    if request.method == 'POST':
        #update company details
        organization.name = request.POST.get('name')
        organization.email = request.POST.get('email')
        organization.phone_no = request.POST.get('phone_no')
        organization.email = request.POST.get('email')
        organization.logo = request.FILES.get('logo')
        organization.address = request.POST.get('address')
        organization.save()
        return redirect('home')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': organization.name,
            'email': organization.email,
            'phone_no': organization.phone_no,
            'email': organization.email,
            'logo': organization.logo,
            'address': organization.address,
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

        form_mpesa = MpesaSettingForm(initial=form_data_mpesa)
        form_sms = SmsForm(initial=form_data_sms)
        form = OrganizationForm(initial=form_data)
        context = {
            'form':form,
            'form_sms':form_sms,
            'form_mpesa':form_mpesa,
            'organization':organization,
            'admins':admins
        }
        return render(request,'company/update-company.html', context)

# -- view to create package
def createPackage(request):
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
def listPackages(request):
    packages = Package.objects.all()
    form = PackageForm()
    context = {'packages':packages, 
                'form':form,
            }        
    return render(request,'company/packages.html', context)
# -- ends

# -- view to list all comapnies
def listCompanies(request):
    companies = Organization.objects.all()
    form = OrganizationForm()
    context = {'companies':companies, 
                'form':form,
            }        
    return render(request,'company/companies.html', context)
# -- ends

# -- view to add sms setting
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