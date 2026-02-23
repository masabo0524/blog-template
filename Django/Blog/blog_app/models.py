from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

#=======================
#=== User management ===
#=======================
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

        
#================================
#=== Base Model for Blog Data ===
#================================
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#==================
#=== Blog Genre ===
#==================
class Topics(BaseModel):
    genre = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.genre)

    class Meta:
        ordering = ["-created_at"]

#=====================
#=== Blog Articles ===
#=====================
class Articles(BaseModel):
    title = models.CharField(max_length=512)
    genre = models.ForeignKey(Topics,
                              on_delete=models.SET_NULL,
                              related_name='articles',
                              null=True)
    limit_reader = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

#===========================
#=== Images for Articles ===
#===========================
def article_directory_path(instance, filename):
    return f"articles/{instance.article_id}/{filename}"

class Images(BaseModel):
    article = models.ForeignKey(Articles,
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to=article_directory_path,
                              width_field='width',
                              height_field='height')
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    def __str__(self):
        return self.article.title

#===========================
#=== Videos for Articles ===
#===========================
class Videos(BaseModel):
    article = models.ForeignKey(Articles,
                                on_delete=models.CASCADE,
                                related_name='videos')
    video = models.FileField(upload_to=article_directory_path)
    
    def __str__(self):
        return self.article.title

#=========================
#=== HTML for Articles ===
#=========================
class Htmls(BaseModel):
    article = models.ForeignKey(Articles,
                                on_delete=models.CASCADE,
                                related_name='htmls')
    html = models.FileField(upload_to=article_directory_path)

    def __str__(self):
        return self.article.title

