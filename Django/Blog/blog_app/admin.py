from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Topics, Articles, Images, Videos, Htmls

Users = get_user_model()
admin.site.register(Users)

admin.site.register(Topics)

admin.site.register(Articles)
admin.site.register(Images)
admin.site.register(Videos)
admin.site.register(Htmls)

