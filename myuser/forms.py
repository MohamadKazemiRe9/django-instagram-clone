from .models import MyUser
from django import forms

class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["username", "photo", "first_name", "last_name", "bio"]