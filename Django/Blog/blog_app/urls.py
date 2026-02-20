from django.urls import path
from .views import HomeView, SignupView

app_name = 'blog_app'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    
]
