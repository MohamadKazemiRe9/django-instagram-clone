from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


from .models import MyUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirm", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone', 'username', 'email', 'first_name', 'last_name')

    def clean_passwords(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("password don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeform(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = MyUser
        fields = ('phone', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', "is_superuser")

class UserAdmin(BaseUserAdmin):
    form = UserChangeform
    add_form = UserCreationForm

    list_display = ('email', 'username', 'phone', 'first_name', 'last_name', "is_staff", 'is_admin')
    list_filter = ('is_admin', "is_staff")

    fieldsets = (
        (None, {'fields':('email', 'username', 'password')}),
        ('Personal info', {"fields":('first_name', 'last_name', "phone", "photo", "date_of_birth")}),
        ('Permissions', {'fields':("is_active","is_staff", "is_admin", "is_superuser")})
    )
    search_fields = ['email', "phone", "username"]
    filter_horizontal = ()
    

admin.site.register(MyUser, UserAdmin)
