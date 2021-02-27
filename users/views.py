from django.shortcuts import render
from .forms import OpticaRegisterForm
from django.shortcuts import redirect

# Create your views here.
def signup(request):
    if request.method=='POST':
        optica_form = OpticaRegisterForm(request.POST)
        if optica_form.is_valid():
            print(optica_form.cleaned_data)
            optica_form.save()
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

