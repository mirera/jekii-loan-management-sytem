
from multiprocessing import context
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CompanyStaffForm
from django.contrib import messages
from .models import CompanyStaff, Role
from branch.models import Branch
from company.models import Organization


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
        #elif user.user_type == 'staff':
            #return redirect('dashboard')
        else:
            return redirect('home')


    #extracting login credential from login form
    if request.method == 'POST':
        username = request.POST.get('username')
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
               # elif user.user_type == 'staff':
                   # return redirect('dashboard')
                else:
                    return redirect('home')
        else:
            messages.error(request, 'The username or password is incorrect')
            
    return render (request, 'user/auth-login.html')

#---user login in logic ends here---

#---user register  logic starts here---
def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':

        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        #binding data from fields to the form
        form = CustomUserCreationForm(request.POST)

        #performing validation
        if form.is_valid():

            #save user but no commit before lowercasing the username
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User created successfully!')
 
            #create a company object 
            organization = Organization.objects.create(
               name = company_name,
               email = email,
               admin = user
            )
            
            #create default branch object 
            today = datetime.today().strftime('%Y-%m-%d')
            default_branch = Branch.objects.create(
                company = organization,
                name = 'Main Branch',
                open_date = today,
                capital = '2000000',
                office = '123 HeadQuater Street'
            )

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
            )
            #redirect to update organization info
            return redirect('update-organization', pk = organization.id )
        else:
            #return error message
            messages.error(request, 'An error occured during regetration, please try again!')

    context= {form:'form'}

    return render (request, 'user/auth-register.html', context)
#--- ends---

def password_reset(request):
    return render(request, 'user/auth-reset.html')

def user_logout(request):
    logout(request)
    return redirect('home')

#-- list staffs view starts --
def listStaff(request):
    
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None
        
    staffs = CompanyStaff.objects.filter(company=company).order_by('date_added')
    form = CompanyStaffForm(request.POST, company=company) 

    context = {'staffs': staffs, 'form':form}
    return render(request, 'user/users-list.html', context)
#-- end -- 

#-- adding a staff then as a user --
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

        password = make_password(request.POST.get('password'))  # Hash the password

        CompanyStaff.objects.create(
            company = company,
            username = request.POST.get('username'),
            password = password, 
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            email= request.POST.get('email'),
            id_no= request.POST.get('id_no'),
            phone_no = request.POST.get('phone_no'),
            branch = branch,
            user_type= request.POST.get('user_type'),
            staff_role = role,
            profile_photo=request.FILES.get('profile_photo')
        )
        #signing up the created user
        User.objects.create(
            username = request.POST.get('username'),
            password = password,
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            email = request.POST.get('email'),
        )
        
        return redirect('staffs') #users view

    
    context= {'form':form}
    return render(request,'user/users-list.html', context)
#-- end --

# -- update userprofile
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

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.id_no = request.POST.get('id_no')
        user.phone_no = request.POST.get('phone_no')
        user.save()

        return redirect('profile')
    else:

        form_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id_no': user.id_no,
            'phone_no': user.phone_no,
            'email': user.email,
        }

        form = CompanyStaffForm(initial=form_data)
        return render(request,'user/user-profile.html',{'form':form, 'user':user})
# -- ends

 
