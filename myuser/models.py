from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator



class MyUserManager(BaseUserManager):
    def create_user(self, phone, username, email, first_name, last_name, password=None):
        if not phone:
            raise ValueError("You have import phone number")
        if not username:
            raise ValueError("You have to import username")
        if not email:
            raise ValueError("You must to import Email address")

        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email, first_name="", last_name="", password=None):
        user = self.create_user(
            phone = phone,
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True, 
        validators=[
            RegexValidator(regex="\A(09)(0|1|2|3)[0-9]{7}\d\Z", message="phone number is not correct")
        ])
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", default="users/default.jpg")
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField("self", through="Contact", related_name="followers", symmetrical=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email']

    

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Contact(models.Model):
    user_from = models.ForeignKey(MyUser, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(MyUser, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_from} follows {self.user_to}"