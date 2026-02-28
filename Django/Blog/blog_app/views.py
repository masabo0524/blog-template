from django.shortcuts import render
from django.urls import reverse_lazy
import os

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .forms import CustomUserCreationForm, PostArticleForm
from .models import Users, Topics, Articles, Htmls, Images, Videos, Audios
from .Mixin import OnlySuperUserMixin
from .change_path_html import Screening_path, file2str

#================
#=== Top Page ===
#================
class HomeView(TemplateView):
    template_name = 'home.html'
    
#===================
#=== Singup page ===
#===================
class SignupView(CreateView):
    model = Users
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog_app:home')
    template_name = 'signup.html'

    def form_valid(self, form):
        login(self.request, self.object)
        return super().form_valid(form)

#===================
#=== Logout page ===
#===================
class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('blog_app:home')

#==================
#=== Login page ===
#==================
class LoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy('blog_app:home')


#=========================
#=== Article List page ===
#=========================
class BlogListView(ListView):
    template_name = 'blog_list.html'
    Model = Articles
    context_object_name = 'articles'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        topic_id = self.kwargs.get(self.slug_url_kwarg)
        article_list = Articles.objects.filter(genre_id=topic_id, public=True).prefetch_related('images',
                                                                                   'videos',
                                                                                   'htmls')
        return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id = self.kwargs.get(self.slug_url_kwarg)
        topic_name = Topics.objects.get(pk=topic_id)
        context['topic'] = topic_name
        return context

#=========================
#=== Post article View ===
#=========================
class PostArticleView(OnlySuperUserMixin, FormView):
    template_name = "PostArticle.html"
    form_class = PostArticleForm
    success_url = reverse_lazy('blog_app:home')
    context_object_name = 'post_form'

    def form_valid(self, form):
        article_title = form.cleaned_data.get("title")
        article_genre = form.cleaned_data.get("genre")
        article_summary = form.cleaned_data.get("summary")
        files = form.cleaned_data.get("html_file")
        is_limited = form.cleaned_data.get("is_limited")
        article = Articles(title=article_title,
                           genre=article_genre,
                           summary=article_summary)
        article.save()

        for_save_folder = "/masaaki/desktop/"

        html_files = []
        media_path = ""
        for file_data in files:
            if file_data.content_type == "text/html":
                html_files.append(file_data)
                print(html_files)
            elif 'image' in file_data.content_type:
                image_obj = Images(article=article,
                                   image=file_data)
                image_obj.save()
                media_path = image_obj.image.url
                
            elif 'video' in file_data.content_type:
                video_obj = Videos(article=article,
                                   video=file_data)
                video_obj.save()
                media_path = vide_obj.video.url
                
            elif 'audio' in file_data.content_type:
                audio_obj = Audios(article=article,
                                   audio=file_data)
                audio_obj.save()
                media_path = audio_obj.audio.url

        if not media_path:
            for html_file in html_files:
                html_db = file2str(html_file)
                html_obj = Htmls(article=article,
                                 html=html_db)
                html_obj.save()
        else:
            media_path = os.path.dirname(media_path)
            for html_file in html_files:
                html_db = Screening_path(html_file, media_path)
                html_obj = Htmls(article=article,
                                 html=html_db)
                html_obj.save()

        return super().form_valid(form)


#========================
#=== Blog Detail View ===
#========================
class ArticleDetailView(DetailView):
    model = Articles
    template_name = "blog.html"
    pk_url_kwarg = "article_id"
    context_object_name = "htmlfile"
    queryset = Articles.objects.prefetch_related('htmls')

