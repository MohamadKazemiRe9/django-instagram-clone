from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("You are loged in")
                else:
                    return HttpResponse("Your account is not active")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')

def regsiter(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            phone = form.cleaned_data["phone"]
            if password == password2:
                user.set_password(password)
            else:
                form = RegistrationForm(initial={'phone':phone, })
                return render(request, 'account/register.html', {"form":form})
            user.save()
            return render(request, 'account/register_done.html',{'user':user})
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {"form":form})