from django.shortcuts import render
from posts.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import JsonResponse
# Create your views here.

def home(request):
    user = request.user
    my_posts = Post.objects.filter(user=user).order_by("-created")
    posts = Post.objects.none()
    if user.following.all():
        for friend in user.following.all():
            friends_posts = Post.objects.filter(user=friend)
            posts = (my_posts | friends_posts)
    else:
        posts = my_posts

    paginator = Paginator(posts, 6)
    try:
        page = request.GET.get("page")
        if page:
            print(page)
            posts = paginator.page(page)
            print(posts)
            return JsonResponse({
                "status":render_to_string("pages/ajax_posts.html", {"posts":posts}, request=request)
            })
        else:
            posts = paginator.page(1)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        return JsonResponse({"status":"empty"})
    return render(request, "pages/home.html", {"posts":posts})