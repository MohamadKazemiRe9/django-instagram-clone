from django.shortcuts import render, redirect
from .forms import UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def edit(request):
    if request.method=="POST":
        form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile", request.user)
        else:
            messages.error(request, "Error updating your profile")
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'form':form})
