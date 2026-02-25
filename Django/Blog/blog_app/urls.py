from django.urls import path
from .views import HomeView, SignupView, LogoutView, LoginView, BlogListView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog_app'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('blogs/<int:id>/', BlogListView.as_view(), name='blogs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

