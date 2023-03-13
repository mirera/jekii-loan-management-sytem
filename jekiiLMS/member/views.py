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

# list member view starts 
def listMembers(request):
    members = Member.objects.all().order_by('date_joined')
    form = MemberForm()

    #later on add a loan context so as to utilize them on the member table.
    context = {'members': members, 'form':form}
    return render(request, 'member/members-list.html', context)

# list member view ends

# view member view starts 
def viewMember(request, pk):
    member = Member.objects.get(id=pk)

    context = {'member': member}
    return render(request, 'member/member-view.html', context)

# view member view ends

# delete member view starts 
def deleteMember(request,pk):
    member = Member.objects.get(id=pk)

    if request.method == 'POST':
        member.delete()
        return redirect('members')

     #context is {'obj':branch}, in delete.html we are accessing room/message as 'obj'
    context = {'obj':member}
    return render(request,'member/delete-member.html', context)

# delete member ends starts

#edit member view starts
def editMember(request,pk):
    member = Member.objects.get(id=pk)
    
    if request.method == 'POST':
        # update the branch with the submitted form data
        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.id_no = request.POST.get('id_no')
        member.phone_no = request.POST.get('phone_no')
        member.email = request.POST.get('email')
        member.branch = request.POST.get('branch')
        member.business_name = request.POST.get('business_name')
        member.industry = request.POST.get('industry')
        member.address = request.POST.get('address')
        member.credit_score = request.POST.get('credit_score')
        member.passport_photo = request.POST.get('passport_photo')

        

        member.save()

        return redirect('members')
    else:
        # prepopulate the form with existing data
        form_data = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'id_no': member.id_no,
            'phone_no': member.phone_no,
            'email': member.email,
            'branch': member.branch,
            'business_name': member.business_name,
            'industry': member.industry,
            'address': member.address,
            'credit_score': member.credit_score,
            'passport_photo': member.passport_photo,
        }
        form = MemberForm(initial=form_data)
        return render(request,'member/edit-member.html',{'form':form})

#edit member view ends    