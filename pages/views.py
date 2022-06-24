from django.shortcuts import render
from posts.models import Post
# Create your views here.

def home(request):
    user = request.user
    my_posts = Post.objects.filter(user=user).order_by("-created")
    posts = Post.objects.none()
    for friend in user.following.all():
        friends_posts = Post.objects.filter(user=friend)
        posts = (my_posts | friends_posts)[:6]
    return render(request, "pages/home.html", {"posts":posts})