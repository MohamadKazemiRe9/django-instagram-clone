from dataclasses import fields
from django import forms
from .models import Post, PostComment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ["text"]