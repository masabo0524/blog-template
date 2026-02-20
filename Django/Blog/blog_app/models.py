from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Please enter your email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('Please enter your email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('blog_app:home')

    class Meta:
        db_table = 'User_list'
