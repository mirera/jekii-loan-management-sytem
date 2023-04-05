
from multiprocessing import context
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CompanyStaffForm
from django.contrib import messages
from .models import CompanyStaff, Role
from branch.models import Branch
from company.models import Organization


#---user login in logic starts here---

def user_login(request):
    #preventing logged in users from logging in again   
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff: 
            return redirect('superadmin_dashboard')
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
    staffs = CompanyStaff.objects.all().order_by('date_added')
    form = CompanyStaffForm()

    context = {'staffs': staffs, 'form':form}
    return render(request, 'user/users-list.html', context)
#-- end -- 

#-- adding a staff then as a user --
def addStaff(request):
    form = CompanyStaffForm()
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        branch = Branch.objects.get(pk=branch_id)

        role_id = request.POST.get('staff_role')
        role = Role.objects.get(pk=role_id)

        password = make_password(request.POST.get('password'))  # Hash the password

        CompanyStaff.objects.create(
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

 
