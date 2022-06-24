from ast import expr_context
from turtle import pos
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, PostCommentForm
from .models import Post, PostComment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from actions.utils import create_action


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
            create_action(request.user, "posted", new_obj)
            return redirect("profile", request.user)
    else:
        form = PostCreateForm()
    return render(request, "posts/create.html", {"form":form})



def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    form = PostCommentForm()
    if request.method == "POST":
        try:
            action = request.POST.get("action")
            comment_id = request.POST.get("id")
        except:
            action = None
            comment_id = None
        if action and comment_id:
            try:
                comment = PostComment.objects.get(id=comment_id)
                if action == "like":
                    comment.likes.add(request.user)
                else:
                    comment.likes.remove(request.user)
                return JsonResponse({"status":"OK"})
            except:
                return JsonResponse({"status":"error"})

        else:
            form = PostCommentForm(request.POST)
            if form.is_valid():
                try:
                    new_comment = form.save(commit=False)
                    new_comment.user = request.user
                    new_comment.post = post
                    new_comment.save()
                    form = PostCommentForm()
                    return JsonResponse({'status':"ok", "id":new_comment.id})
                except:
                    return JsonResponse({'status':"error"})
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
                create_action(request.user, "likes", post)
            else:
                post.user_like.remove(request.user)
                create_action(request.user, "dislikes", post)
            return JsonResponse({'status':"ok"})
        except:
            pass
        return JsonResponse({'status':"error"})