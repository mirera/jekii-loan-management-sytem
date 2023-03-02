from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member 
from .forms import MemberForm

#create member view starts
def createMember(request):
    form = MemberForm()
    #processing the data
    if request.method == 'POST':
        Member.objects.create(
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            id_no= request.POST.get('id_no'),
            phone_no = request.POST.get('phone_no'),
            branch = request.POST.get('branch'),
            email= request.POST.get('email'),
            business_name = request.POST.get('business_name'),
            industry = request.POST.get('industry'),
            address = request.POST.get('address'),
            passport_photo = request.POST.get('passport_photo')
        )
        #redirecting user to branches page(url name) after submitting form
        return redirect('members')

    
    context= {'form':form}
    return render(request,'member/create-member.html', context)
#create member view ends
