from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm
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