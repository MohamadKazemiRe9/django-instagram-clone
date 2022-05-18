from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, VerifyRegsitration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import randint
from . import info
import requests
import datetime, time
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
                    messages.success(request, "You are logged in successfully!")
                    return render(request, "account/dashboard.html", {})
                else:
                    return HttpResponse("Your account is not active")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})

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
                messages.error(request, "passwords dosn't match!")
                return render(request, 'account/register.html', {"form":form})
            user.save()
            login(request, user)
            verify_code = randint(11111,99999)
            request.session["verify"] = verify_code
            send_sms(request, phone, verify_code)
            return redirect("verify")
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {"form":form})

def verify_register(request):
    if request.method == "POST":
        form = VerifyRegsitration(request.POST)
        if form.is_valid():
            verify_code = form.cleaned_data["code"]
            if verify_code == request.session["verify"]:
                user = request.user
                user.is_verify = True
                user.save()
                return render(request, 'account/register_done.html',{'user':user})
            else:
                messages.error(request, "your code in not correct")
    else:
        form = VerifyRegsitration()
        return render(request, "account/verify.html", {'form':form})

def resend_sms(request):
    t = datetime.datetime.now()
    end = time.mktime(t.timetuple())
    start = request.session.get("time_start")
    if end - start > 120:
        send_sms(request, request.user.phone, request.session["verify"])
        messages.success(request, "messege resended agian")
    else:
        messages.error(request, "You must wiat at least 2 minutes")
    return redirect("verify")
    

def send_sms(request, phone, code):
    api_key = info.api_key
    url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json?receptor={phone}&sender=2000500666&message={code}"
    result = requests.get(url)
    t = datetime.datetime.now()
    start = time.mktime(t.timetuple())
    request.session["time_start"] = start