from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from jekiiLMS.decorators import permission_required
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Permission
from jekiiLMS.format_inputs import format_phone_number, deformat_phone_no
from .forms import CustomUserCreationForm, CompanyStaffForm , RoleForm
from django.contrib import messages
from .models import CompanyStaff, Role
from branch.models import Branch 
from user.models import Notification
from company.models import Organization, Package, SmsSetting
from jekiiLMS.sms_messages import send_sms 


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

        if user is not None:
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
            
    return render (request, 'user/auth-login.html')

#---user login in logic ends here---

#---user register  logic starts here---
def user_signup(request):
    #binding data from fields to the form
    form = CustomUserCreationForm(request.POST)

    if request.method == 'POST':

        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        

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
            #user.save()    
            login(request, user)
            messages.success(request, 'User created successfully!')

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
                notes = 'This is the default branch. Do not delete'
            )

            # Create default Role for Company admin, all permissions
            permissions = Permission.objects.filter(
                    content_type__model__in=['branch', 'expense category', 'expense',
                                            'member', 'loanproduct', 'loan', 'repayment',
                                            'collateral', 'guarantor', 'companyadmin',
                                            'companystaff', 'role', 'note']
                )

            role = Role(
                company=organization,
                name=organization.name + '-admin',
                description='This is the default role of the admin user. They have all the permissions'
            )
            role.save()
            # Assign the retrieved permissions to the role using the set() method
            role.permissions.set(permissions)

            #create a staff object of the admin
            password = make_password(request.POST.get('password1'))
            staff = CompanyStaff.objects.create(
                company = organization,
                username = request.POST.get('username'),
                password = password,
                email = email,
                first_name = request.POST.get('username'),
                last_name = request.POST.get('username'),
                branch = default_branch,
                user_type = 'admin',
                staff_role = role
            )
            #send email to for email verification 
            context = {'company_name':company_name}
            template = render_to_string('user/company_welcome.html', context)
            email = EmailMessage(
                "Welcome to Loginit",
                template,
                settings.EMAIL_HOST_USER  ,
                [email],
                reply_to=[settings.EMAIL_HOST_USER],
            )
            email.send(fail_silently=False)

            #redirect to update organization info
            messages.success(request, f'Account for {company_name} was created successfully. Check your {email} for verification instructions')
            return redirect('update-organization', pk = organization.id )
        else:
            #return error message
            messages.error(request, 'An error occured during regetration, please try again!')

    context= {'form':form}
    return render (request, 'user/auth-register.html', context)
#--- ends---

@login_required(login_url='login')
def password_reset(request):
    return render(request, 'user/auth-reset.html')

def user_logout(request):
    logout(request)
    return redirect('home')

#-- list staffs view starts --
@login_required(login_url='login')
def listStaff(request):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    staffs = CompanyStaff.objects.filter(company=company).order_by('date_added')[1:] #xclude main admin
    form = CompanyStaffForm(request.POST, company=company) 

    context = {'staffs': staffs, 'form':form}
    return render(request, 'user/users-list.html', context)
#-- end -- 

#-- adding a staff then as a user --
@login_required(login_url='login')
@permission_required('user.add_user')
def addStaff(request):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
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
#@permission_required('user.view_user')
def view_staff(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
            
    staff_user = CompanyStaff.objects.get(id=pk, company=company)
    context = {'staff_user':staff_user}
    return render(request, 'user/view-staff.html', context)
# -- ends --


# -- delete staff --
@login_required(login_url='login')
@permission_required('user.delete_user')
def deleteStaff(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
            
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
#@permission_required('user.change_user')
def update_user_profile(request):
        
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

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
#@permission_required('user.change_user')
def change_photo(request):
        
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

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
#@permission_required('user.change_user')
def updateStaff(request, pk):
        
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

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
    staff.status = 'inactive'
    user.is_active= False
    user.save()
    staff.save()

    #send sms
    sms_setting = SmsSetting.objects.get(company=company)
    sender_id = sms_setting.sender_id
    token = sms_setting.api_token 
    message = f"Dear {staff.first_name}, Your {company.name} user account has been deactivated. Contact your system admin"
    send_sms(
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
    send_sms(
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
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

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
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

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
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None

  
    roles = Role.objects.filter(company=company).order_by('date_added')
    form = RoleForm(request.POST) 
    context = {'roles': roles, 'form':form, 'permissions':permissions}
    return render(request, 'user/roles-list.html', context)
# -- ends --

# -- delete role --
@login_required(login_url='login')
@permission_required('user.delete_role')
def deleteRole(request,pk):

    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
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



