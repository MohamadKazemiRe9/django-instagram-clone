from ast import expr_context
from turtle import pos
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, PostCommentForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse


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
    form = PostCommentForm()
    if request.method == "POST":
        form = PostCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            form = PostCommentForm()
            return render(request, "posts/detail.html", {"post":post, "form":form})
    else:
        return render(request, "posts/detail.html", {"post":post, "form":form})

@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get("id")
    action = request.POST.get("action")
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == "like":
                post.user_like.add(request.user)
            else:
                post.user_like.remove(request.user)
            return JsonResponse({'status':"ok"})
        except:
            pass
        return JsonResponse({'status':"error"})