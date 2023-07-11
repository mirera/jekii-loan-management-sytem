from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from jekiiLMS.decorators import permission_required
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Permission
from jekiiLMS.format_inputs import format_phone_number, deformat_phone_no
from .forms import CustomUserCreationForm, CompanyStaffForm , RoleForm
from .models import CompanyStaff, Role
from branch.models import Branch 
from user.models import Notification
from company.models import Organization, Package, SmsSetting, SystemSetting, SecuritySetting
from jekiiLMS.sms_messages import send_sms
from jekiiLMS.tasks import send_email_task, send_sms_task
from jekiiLMS.utils import get_user_company
import pyotp


#---user login in logic starts here---
def user_login(request):
    #preventing logged in users from logging in again
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username)
        except CompanyStaff.DoesNotExist:
            pass

        if request.user.is_superuser or request.user.is_staff: 
            return redirect('superadmin_dashboard')
        else:
            return redirect('home')
        
    #extracting login credential from login form
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #raise username do not exist in our databse error
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This username does not exist on our database!')

        # check if username and password match to autheticate
        user = authenticate(username=username, password=password)

        #check if the user is email-verified
        try:
            staff = CompanyStaff.objects.get(username=user.username)#check if user is client-staff
        except:
            staff = 'something' # find out our to include the super user/staff with their phone no.

        if staff.is_verified: 
            if user is not None:
                security_settings = SecuritySetting.objects.get(company=staff.company)
                if security_settings.two_fa_auth:
                    # Generate the time-bound OTP
                    totp = pyotp.TOTP(settings.OTP_SECRET_KEY)
                    system_otp = totp.now()

                    #append otp and user id to the session
                    request.session['otp'] = system_otp
                    request.session['pk'] = user.id

                    #check is user is client-staff or loginit-staff
                    try:
                        staff = CompanyStaff.objects.get(username=user.username)#check if user is client-staff
                    except:
                        staff = 'something' # find out our to include the super user/staff with their phone no. 
                    #send OTP as SMS
                    sender_id = settings.SMS_SENDER_ID
                    token = settings.SMS_API_TOKEN
                    message = f"Your OTP is {system_otp}. It will be active for the next 02.00 minutes."
                    send_sms_task.delay(
                        sender_id,
                        token,
                        staff.phone_no, 
                        message,
                        )
                    #redirect user to Enter OTP form page
                    return redirect('input_otp')
                else:
                    #login and redirect home page
                    login(request, user)
                    if request.user.is_authenticated and request.user.is_active:
                        try:
                            user = CompanyStaff.objects.get(username=request.user.username)
                        except CompanyStaff.DoesNotExist:
                            pass
                            
                        if request.user.is_superuser or request.user.is_staff: 
                            return redirect('superadmin_dashboard')
                        else:
                            return redirect('home') 
            else:
                messages.error(request, 'The username or password is incorrect')
        else:
            messages.info(request, 'Your email is not verified. Check your email and verify.')
    return render (request, 'user/auth-login.html')
#---user login in logic ends here---

#input OTP
def input_otp(request):
    return render(request,'user/input-otp.html')
#-- ends

#send OTP to email instead
def otp_to_email(request, uid):
    # Generate the time-bound OTP
    totp = pyotp.TOTP(settings.OTP_SECRET_KEY)
    system_otp = totp.now()

    user = get_object_or_404(User, id=request.session['pk'])

    context = {
        'otp':system_otp,
        'user':user.username
    }
    #send email for email verification 
    send_email_task.delay(
        context=context,
        template_path='user/to-email-otp.html',
        from_name='Mdeni',
        from_email=settings.EMAIL_HOST_USER,
        subject='Mdeni OTP for Login',
        recipient_email=user.email,
        replyto_email=settings.EMAIL_HOST_USER
    )
    #redirect user to Enter OTP form page
    return redirect('input_otp')
#-- end

#resend OTP to sms
def resend_otp(request, uid):
    # Generate the time-bound OTP
    totp = pyotp.TOTP(settings.OTP_SECRET_KEY)
    system_otp = totp.now()

    user = get_object_or_404(User, id=request.session['pk'])

    #check is user is client-staff or loginit-staff
    try:
        staff = CompanyStaff.objects.get(username=user.username)
    except:
        staff = 'something' # find out our to include the super user/staff with their phone no. 
    #send OTP as SMS
    sender_id = settings.SMS_SENDER_ID
    token = settings.SMS_API_TOKEN
    message = f"Your OTP is {system_otp}. It will be active for the next 02.00 minutes."
    send_sms_task.delay(
        sender_id,
        token,
        staff.phone_no, 
        message,
        )
    #redirect user to Enter OTP form page
    return redirect('input_otp')
#-- end

#OTP verify
def verify(request):
    if request.method == 'POST':
        #get the user pk from request.session('pk')
        user = get_object_or_404(User, id=request.session['pk'])
        otp = int(request.POST.get('otp')) 

        #get system generated otp from session
        totp = pyotp.TOTP(settings.OTP_SECRET_KEY)

        #verify otp
        if totp.verify(otp):
            #login and redirect home page
            login(request, user)
            if request.user.is_authenticated and request.user.is_active:
                try:
                    user = CompanyStaff.objects.get(username=request.user.username)
                except CompanyStaff.DoesNotExist:
                    pass
                    
                if request.user.is_superuser or request.user.is_staff: 
                    return redirect('superadmin_dashboard')
                else:
                    return redirect('home')
        else:
            #else redirect Enter OTP page 
            messages.error(request, 'Invalid OTP!')
            return redirect('input_otp')
    
    return redirect('login')
#-- ends

#---user register  logic starts here---
def user_signup(request):
    form = CustomUserCreationForm(request.POST)
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        #phone_no = request.POST.get('phone_no')
        #formated_phone_no = format_phone_number(phone_no, company.phone_code)
        
        email = request.POST.get('email')

        # Check if email exists in the system
        r = User.objects.filter(email=email)
        if r.count():
            messages.error(request, "Email already exists")

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'The passwords do not match! Try again.')
        else:
            # Check password strength
            if len(password1) < 8:
                messages.error(request, 'Your password must be at least 8 characters long.')
            elif password1.isdigit():
                messages.error(request, 'Your password must contain at least one letter.')
            elif password1.isalpha():
                messages.error(request, 'Your password must contain at least one digit.')
            else:
                # Hash the new password
                password = make_password(password1)

        #performing validation
        if form.is_valid():
            #save user but no commit before lowercasing the username
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # assign Company admin user, all permissions 
            permissions = Permission.objects.filter(
                    content_type__model__in=['branch', 'expense category', 'expense',
                                            'member', 'loanproduct', 'loan', 'repayment',
                                            'collateral', 'organization', 'guarantor', 'companyadmin',
                                            'companystaff', 'role', 'note','smssetting',
                                             'mpesasetting', 'emailsetting']
                )
            user.user_permissions.add(*permissions)

            package_name = 'Free Trial'
            package = Package.objects.get(name=package_name)

            #create a company object 
            organization = Organization.objects.create(
               name = company_name,
               email = email,
               admin = user,
               package = package
            ) 
            
            #create default branch object 
            today = datetime.today().strftime('%Y-%m-%d')
            default_branch = Branch.objects.create(
                company = organization,
                name = 'Main Branch',
                email = email,
                open_date = today,
                capital = '2000000',
                office = '123 HeadQuater Street',
                notes = 'This is the default branch. DO NOT DELETE!'
            )

            # Create default Role for Company admin, all permissions
            permissions = Permission.objects.filter(
                    content_type__model__in=['branch', 'expense category', 'expense',
                                            'member', 'loanproduct', 'loan', 'repayment',
                                            'collateral', 'organization', 'guarantor', 'companyadmin',
                                            'companystaff', 'role', 'note','smssetting',
                                             'mpesasetting', 'emailsetting']
                )

            role = Role(
                company=organization,
                name=organization.name + '-admin',
                description='This is the default role of the admin user. They have all the permissions. DO NOT DELETE!'
            )
            role.save()
            # Assign the retrieved permissions to the role using the set() method
            role.permissions.set(permissions)

            #create a staff object of the admin
            staff = CompanyStaff.objects.create(
                company = organization,
                username = request.POST.get('username'),
                password = password,
                email = email,
                #phone_no = phone_no
                first_name = request.POST.get('username'),
                last_name = request.POST.get('username'),
                branch = default_branch,
                user_type = 'admin',
                staff_role = role
            )

            # activate email token generator
            token_generator = PasswordResetTokenGenerator()
            verify_email_url = request.build_absolute_uri(reverse('verify-email', args=[user.id, token_generator.make_token(user)])) 
            context = {
                'company_name':company_name,
                'user':user.username,
                'verify_email_url':verify_email_url
                }
            
            #send welcome email 
            send_email_task.delay(
                context=context,
                template_path='user/company_welcome.html',
                from_name='Mdeni',
                from_email=settings.EMAIL_HOST_USER,
                subject='Welcome to Mdeni',
                recipient_email=email,
                replyto_email=settings.EMAIL_HOST_USER
            )

            #send email for email verification 
            send_email_task.delay(
                context=context,
                template_path='user/verify-emailtemplate.html',
                from_name='Mdeni',
                from_email=settings.EMAIL_HOST_USER,
                subject='Verify Your Email',
                recipient_email=email,
                replyto_email=settings.EMAIL_HOST_USER
            )
            messages.success(request, 'User created successfully! Please check your email for acount verification.')
            return render(request, 'user/verify-email.html')
        else:
            messages.error(request, 'An error occured during regetration, please try again!')

    context= {'form':form}
    return render (request, 'user/auth-register.html', context)
#--- ends---

#-- resend email verification token incase it expires
def resend_email_token(request, uid):
    #retrieve the user requesting for resend
    try:
        user = User.objects.get(id=uid)
    except:
        user = None
    #activate email token generator
    token_generator = PasswordResetTokenGenerator()
    verify_email_url = request.build_absolute_uri(reverse('verify-email', args=[user.id, token_generator.make_token(user)])) 
    context = {
        'user':user.username,
        'verify_email_url':verify_email_url
        }
    #send email for email verification 
    send_email_task.delay(
        context=context,
        template_path='user/verify-emailtemplate.html',
        from_name='Mdeni',
        from_email=settings.EMAIL_HOST_USER,
        subject='Verify Your Email',
        recipient_email=user.email,
        replyto_email=settings.EMAIL_HOST_USER
    )
    messages.success(request, 'Please check your email for account verification.')
    return render(request, 'user/verify-email.html') 
#-- ends          
#--verify email view
def verify_email(request, uid, token):
    # Retrieve the user using the uid
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        user = None

    if user is not None:
        # Verify the token
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            # Token is valid
            try:
                staff = CompanyStaff.objects.get(username=user.username)
                staff.is_verified = True
                staff.save()
                messages.success(request, 'Account successfully verified. Please login.')
                # Redirect to the desired page (e.g., update organization info)
                return redirect('update-organization', pk=staff.company.id)
            except CompanyStaff.DoesNotExist:
                pass
        else:
            # Invalid token
            messages.error(request, 'Invalid token! Please try again.')
            return render(request, 'user/invalid-token.html')
        
    # Invalid user or other error
    messages.error(request, 'Invalid user or other error! Please try again.')
    return render(request, 'user/invalid-token.html')
#-- ends

#-- prompt user to enter email for resetting password
def forgot_password(request):
    return render(request,'user/reset-password.html')
#--ends

# Password reset token generator
token_generator = PasswordResetTokenGenerator()

#-- send change password instructions and link.
def resetpass_email_send(request):
    #get the user email from the POST request
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        #raise email/username do not exist in our database error
        try:
            user = User.objects.get(email=email)
        except:
            user = None
            messages.error(request, 'This email does not exist in our database!')
        if user is not None:
            # Generate the password reset URL parameter user_id and token
            reset_url = request.build_absolute_uri(reverse('password_reset', args=[user.id, token_generator.make_token(user)])) 

            #send the user an email with instruction how to change password and a link 
            context = {
                "user":user.username,
                "reset_url": reset_url
                       }
            send_email_task.delay(
                context=context,
                template_path='user/reset-instructions.html',
                from_name='Mdeni',
                from_email=settings.EMAIL_HOST_USER,
                subject='Mdeni Password Reset',
                recipient_email=email,
                replyto_email=settings.EMAIL_HOST_USER
            )
            messages.success(request, 'Your request for a password reset has been received. Kindly check your email for further instructions.')
            #return render(request,'user/reset-successful.html')
    #return render success 
    return render(request,'user/reset-password.html')
#-- ends

# reset password form
def render_reset_form(request):
    return render(request, 'user/reset-form.html')
#-- ends

# change password

def password_reset(request, pk, token):
    # Retrieve user based on id
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        user=None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'The passwords do not match! Try again.')
            else:
                # Check password strength
                if len(password1) < 8:
                    messages.error(request, 'Your password must be at least 8 characters long.')
                elif password1.isdigit():
                    messages.error(request, 'Your password must contain at least one letter.')
                elif password1.isalpha():
                    messages.error(request, 'Your password must contain at least one digit.')
                else:
                    # Hash the new password
                    password = make_password(password1)
                    user.password = password
                    user.save()

                    #send email to notify user their password was changed recently
                    forgot_password_url = request.build_absolute_uri(reverse('forgot_password')) 
                    context = {
                        "user":user.username,
                        "forgot_password_url": forgot_password_url
                            }
                    send_email_task.delay(
                        context=context,
                        template_path='user/reset-success-email.html',
                        from_name='Mdeni',
                        from_email=settings.EMAIL_HOST_USER,
                        subject='Your Mdeni password has been updated',
                        recipient_email=user.email,
                        replyto_email=settings.EMAIL_HOST_USER
                    )
                    messages.success(request, 'Your password has been successfully reset.')
                    return redirect('login')           
    else:
        messages.error(request, 'Invalid token!')
        return redirect('forgot_password') 
    context = {
        "user":user,
        "token":token
    }
    return render(request, 'user/reset-form.html', context)
    
#-- ends

def user_logout(request):
    logout(request)
    return redirect('home')

#-- list staffs view starts --
@login_required(login_url='login') 
def listStaff(request):
    company = get_user_company(request)  
    staffs = CompanyStaff.objects.filter(company=company).order_by('date_added')[1:] #xclude main admin
    form = CompanyStaffForm(request.POST, company=company) 

    context = {'staffs': staffs, 'form':form}
    return render(request, 'user/users-list.html', context)
#-- end -- 

#-- adding a staff then as a user --
@login_required(login_url='login')
@permission_required('user.add_companystaff')
def addStaff(request):
    company = get_user_company(request) 
    form = CompanyStaffForm(request.POST, company=company) 

    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(pk=branch_id)

        role_id = request.POST.get('staff_role')
        role = Role.objects.get(pk=role_id)

        permissions = role.permissions.all() #retrieve all permissions assigned to a role

        first_name = request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')

        username = request.POST.get('username').lower()
        passcode = request.POST.get('password')
        password = make_password(request.POST.get('password'))  # Hash the password

        phone_no = request.POST.get('phone_no')
        formated_phone_no = format_phone_number(phone_no, company.phone_code)

        CompanyStaff.objects.create(
            company = company,
            username = username,
            password = password, 
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            email= email,
            id_no= request.POST.get('id_no'),
            phone_no = formated_phone_no,
            branch = branch,
            user_type= request.POST.get('user_type'),
            staff_role = role,
            profile_photo=request.FILES.get('profile_photo')
        )
        #signing up the created user
        user = User.objects.create(
            username = username,
            password = password,
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            email = email,
        )
        #assign user role permissions
        user.user_permissions.add(*permissions)

        #send email to for email verification 
        company_name = company.name
        company_email = company.email
        context = {
            'first_name':first_name,
            'last_name':last_name,
            'username':username,
            'passcode':passcode,
            'company_name':company_name,
            'role':role
            }
        from_name_email = f'{company_name} <{settings.EMAIL_HOST_USER}>' 
        template = render_to_string('user/staff-welcome.html', context)
        e_mail = EmailMessage(
            f'Welcome to {company_name}',
            template,
            from_name_email, #'John Doe <john.doe@example.com>'
            [email],
            reply_to=[company_email],
        )
        e_mail.send(fail_silently=False)
        messages.success(request, 'Staff added sucessfully.')
        return redirect('staffs') #users view

    
    context= {'form':form}
    return render(request,'user/users-list.html', context)
#-- end --

# -- view staff --
@login_required(login_url='login')
@permission_required('user.view_companystaff')
def view_staff(request,pk):
    company = get_user_company(request)        
    staff_user = CompanyStaff.objects.get(id=pk, company=company)
    context = {'staff_user':staff_user}
    return render(request, 'user/view-staff.html', context)
# -- ends --


# -- delete staff --
@login_required(login_url='login')
@permission_required('user.delete_companystaff')
def deleteStaff(request,pk):
    company = get_user_company(request)      
    if request.method == 'POST':
        staff = CompanyStaff.objects.get(id=pk, company=company)
        user = User.objects.get(username=staff.username)
        staff.delete()
        user.delete()
        messages.success(request, 'Staff & User deleted successfully!')
        return redirect('staffs')

    return render(request, 'user/users-list.html')
# -- ends --

# -- update userprofile
@login_required(login_url='login')
def update_user_profile(request): 
    company = get_user_company(request) 
    user = CompanyStaff.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        formated_phone_no = format_phone_number(phone_no,company.phone_code)
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.id_no = request.POST.get('id_no')
        user.phone_no = formated_phone_no
        user.save()

        return redirect('profile')
    else:
        deheaded_phone = deformat_phone_no(user.phone_no, user.company.phone_code)
        form_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id_no': user.id_no,
            'phone_no': deheaded_phone,
            'email': user.email,
        }

        form = CompanyStaffForm(initial=form_data)
        return render(request,'user/user-profile.html',{'form':form, 'user':user})
# -- ends

# --  user change photo
@login_required(login_url='login')
def change_photo(request):
    user = CompanyStaff.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        user.profile_photo = request.FILES.get('profile_photo')
        user.save()

        return redirect('profile')
    else:
        form_data = {
            'profile_photo': user.profile_photo,
        }

        form = CompanyStaffForm(initial=form_data)
        return render(request,'user/user-profile.html',{'form':form, 'user':user})
# -- ends

# -- edit user/staff
@login_required(login_url='login')
@permission_required('user.change_companystaff')
def updateStaff(request, pk):
    company = get_user_company(request) 
    staff = CompanyStaff.objects.get(id=pk, company=company)
    user = User.objects.get(username=staff.username)
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(id=branch_id)

        role_id = request.POST.get('staff_role')
        staff_role = Role.objects.get(id=role_id)

        phone_no = request.POST.get('phone_no')
        formated_phone_no = format_phone_number(phone_no, company.phone_code) 

        staff.company= company
        staff.username = request.POST.get('username').lower()
        staff.email = request.POST.get('email')
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.id_no = request.POST.get('id_no')
        staff.phone_no = formated_phone_no
        staff.branch = branch
        staff.user_type = request.POST.get('user_type')
        staff.staff_role = staff_role
        staff.save()

        #since the companystaff is linked to user obj via username update user.username
        user.username = staff.username
        user.save()

        return redirect('staffs')
    else:
        deheaded_phone = deformat_phone_no(staff.phone_no, staff.company.phone_code)
        form_data = {
            'username':staff.username,
            'email':staff.email,
            'first_name': staff.first_name,
            'last_name': staff.last_name,
            'id_no': staff.id_no,
            'phone_no': deheaded_phone, 
            'branch':staff.branch,
            'user_type':staff.user_type,
            'staff_role':staff.staff_role,
            'email': staff.email,
        }
    
        form = CompanyStaffForm(initial=form_data, company=company)

        return render(request,'user/update-staff.html',{'form':form, 'staff':staff})
# -- ends 

# -- view to deactivate a staff
@login_required(login_url='login')
@permission_required('user.deactivate_user')
def deactivateStaff(request, pk):
    staff = CompanyStaff.objects.get(id=pk)
    user = User.objects.get(username=staff.username)
    company = staff.company
    system_preferences = SystemSetting.objects.get(company=company)
    staff.status = 'inactive'
    user.is_active= False
    user.save()
    staff.save()
    
    if system_preferences.is_send_sms:
        #send sms
        sms_setting = SmsSetting.objects.get(company=company) 
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token 
        message = f"Dear {staff.first_name}, Your {company.name} user account has been deactivated. Contact your system admin"
        preferences = SystemSetting.objects.get(company=company)
        if preferences.is_send_sms and sender_id is not None and token is not None:
            send_sms_task.delay(
                sender_id,
                token,
                staff.phone_no, 
                message,
            )

    messages.info(request, 'Staff deactivated! The user will not be able to login in unless activated.')
    return redirect('staffs')
# -- ends

# -- view to activate staff
@login_required(login_url='login')
@permission_required('user.activate_user')
def activateStaff(request, pk):
    staff = CompanyStaff.objects.get(id=pk)
    staff.status = 'active'
    staff.save()

    company = staff.company
    user = User.objects.get(username=staff.username) 
    user.is_active= True
    user.save()
    #send sms
    sms_setting = SmsSetting.objects.get(company=company)
    sender_id = sms_setting.sender_id
    token = sms_setting.api_token 
    message = f"Dear {staff.first_name}, Your {company.name} user account has been activated. You can now login"
    
    preferences = SystemSetting.objects.get(company=company)
    if preferences.is_send_sms and sender_id is not None and token is not None:
        send_sms_task.delay(
        sender_id,
        token,
        staff.phone_no, 
        message,
        )
    messages.info(request, 'Staff activated!')
    return redirect('staffs')
# -- ends

# -- create role --
@login_required(login_url='login')
@permission_required('user.add_role')
def addRole(request):
    # Get all available permissions
    permissions = Permission.objects.filter(
            content_type__model__in=[
                'branch', 'expense category', 'expense',
                'member','loanproduct', 'organization', 
                'loan', 'repayment','collateral', 'guarantor',
                'companyadmin', 'companystaff', 'role', 'note',
                'smssetting','mpesasetting', 'emailsetting' ] 
        )
    company = get_user_company(request) 

    if request.method == 'POST':
        # Create a Role instance with form data
        role = Role(
            company=company,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        role.save()

        # Get the selected permissions from form data
        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(selected_permissions)  # Set the selected permissions to the ManyToManyField

        messages.success(request, 'Role successfully created!')
        return redirect('roles-list')

    context = {'permissions':permissions}    
    return render(request,'user/users-list.html', context)
# -- ends --

# -- edit role --
@login_required(login_url='login')
@permission_required('user.change_role')
def editRole(request, pk):
    company = get_user_company(request) 
    role = Role.objects.get(id=pk, company=company)

    if request.method == 'POST':
        # update the role with the submitted form data
        role.company = company
        role.name = request.POST.get('name')
        role.description = request.POST.get('description')
        role.save()

        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(selected_permissions)

        #update all users with the role permissions
        permissions = role.permissions.all() 
        #get all staff with this role
        staffs = CompanyStaff.objects.filter(company=company, staff_role=role)
        #assign users permissions
        for staff in staffs:
            user = User.objects.get(username=staff.username)
            user.user_permissions.set(permissions)
            user.save()

        messages.success(request, 'Role updated successfully!')
        return redirect('roles-list')

        # update all permissions of user under this role -- mind company specifity

    else:
        # prepopulate the form with existing data
        form_data = {
            'name': role.name,
            'description': role.description,
            'permissions':role.permissions.all()
        }
        form = RoleForm(initial=form_data)

        context = {'form':form, 'role':role}    
        return render(request,'user/edit-role.html', context)
        
# -- ends --

# --  roles list --
@login_required(login_url='login')
def rolesList(request):
    permissions = Permission.objects.filter(
            content_type__model__in=['branch', 'expense category', 'expense',
             'member','loanproduct', 'loan', 'repayment','collateral', 'guarantor',
             'companyadmin', 'companystaff', 'role', 'note' ] 
        )
    company = get_user_company(request) 
    roles = Role.objects.filter(company=company).order_by('date_added')
    form = RoleForm(request.POST) 
    context = {'roles': roles, 'form':form, 'permissions':permissions}
    return render(request, 'user/roles-list.html', context)
# -- ends --

# -- delete role --
@login_required(login_url='login')
@permission_required('user.delete_role')
def deleteRole(request,pk):
    company = get_user_company(request) 
    role = Role.objects.get(id=pk, company=company)    
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully!')
        return redirect('roles-list')

    context = {'obj': role}
    return render(request, 'user/roles-list.html', context)
# -- ends --
 
#mark notfication as read
@login_required(login_url='login')
def mark_notfications_read(request, pk):
    notifications = Notification.objects.filter(recipient=pk, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return redirect('home')



