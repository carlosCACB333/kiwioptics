from django.shortcuts import render
from .forms import OpticaRegisterForm
from django.shortcuts import redirect
from .models import Account, OpticUser, EmployeeUser
from termcolor import colored

# Create your views here.
def signup(request):
    if request.method=='POST':
        optica_form = OpticaRegisterForm(request.POST)
        print(colored(request.POST,'red'))
        if optica_form.is_valid():
            print(colored(optica_form.cleaned_data,'green'))
            new_account = optica_form.save(commit=False)
            new_account.user_type = Account.Types.Optic
            new_account.save()
            OpticUser.objects.create(account = new_account, optic_name=request.POST.get('optic_name'))
            return redirect('users:login')
        else:
            print(optica_form.errors)
            return render(request, 'users/signup.html', {
                'form': optica_form,
            })
    else:
        return render(request, 'users/signup.html', {
        'form':OpticaRegisterForm(),
        })

