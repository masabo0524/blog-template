from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import Users


class HomeView(TemplateView):
    template_name = 'home.html'

class SignupView(CreateView):
    model = Users
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog_app:home')
    template_name = 'signup.html'

