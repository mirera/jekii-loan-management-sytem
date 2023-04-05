from django.shortcuts import render, redirect
from .models import Organization
from .forms import OrganizationForm 

#-- update organization details upon sign up view --
def updateOrganization(request, pk):
    organization = Organization.objects.get(id=pk)
    
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
            'organization':organization
        }
        return render(request,'company/update-company.html', context)