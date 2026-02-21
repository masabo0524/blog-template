from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .forms import CustomUserCreationForm
from .models import Users


class HomeView(TemplateView):
    template_name = 'home.html'

class SignupView(CreateView):
    model = Users
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog_app:home')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('blog_app:home')

class LoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy('blog_app:home')


