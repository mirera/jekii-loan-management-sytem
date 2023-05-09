from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Organization, Package
from .forms import OrganizationForm, PackageForm
from user.models import CompanyStaff , CompanyAdmin

#-- update organization details upon sign up view --
def updateOrganization(request, pk):
    organization = Organization.objects.get(id=pk)
    admins = CompanyStaff.objects.filter(company=organization, user_type='admin')
    
    if request.method == 'POST':
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
        form = OrganizationForm(initial=form_data)
        context = {
            'form':form,
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