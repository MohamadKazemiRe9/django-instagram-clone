from django.shortcuts import render
from .forms import PostCreateForm
from models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_create(request):
    if request.method == "POST":
        pass
    else:
        form = PostCreateForm()
    return render(request, "posts/create.html", {"form":form})