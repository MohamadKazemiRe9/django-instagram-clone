from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm
from .models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def post_create(request):
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.user = request.user
            new_obj.save()
            return redirect("profile", request.user)
    else:
        form = PostCreateForm()
    return render(request, "posts/create.html", {"form":form})

def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    return render(request, "posts/detail.html", {"post":post})