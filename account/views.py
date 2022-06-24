from cmath import log
import json
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from .forms import LoginForm, RegistrationForm, VerifyRegsitration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import randint
from . import info
import requests
import datetime, time
from myuser.models import MyUser, Contact
from posts.forms import PostCreateForm
from posts.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
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
                    return redirect("profile", user)
                else:
                    return HttpResponse("Your account is not active")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})


@login_required
def dashboard(request, username):
    form = PostCreateForm()
    try:
        user = MyUser.objects.get(username=username)
    except:
        return render(request, "account/not_user.html", {})
    posts = Post.objects.filter(user=user).order_by("-created")
    paginator = Paginator(posts, 6)
    try:
        page = request.GET.get("page")
        if page:
            posts = paginator.page(page)
            return JsonResponse({
                "status":render_to_string("account/dashboard_posts_ajax.html", {"posts":posts}, request=request)
            })
        else:
            posts = paginator.page(1)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        return JsonResponse({"status":"empty"})
    return render(request, 'account/dashboard.html', {"user":user, 'form':form, "posts":posts})



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

@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = MyUser.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status":"Ok"})
        except:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})