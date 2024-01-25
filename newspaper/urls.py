"""
URL configuration for newspaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userAuth.views import *
from article.views import *
from category.views import *
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logoutNew, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
  path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  
    path('activate/<int:user_id>/<str:token>/', activate, name='activate'),
    path('', article_list, name='article_list'),
    path('<int:article_id>/', article_detail, name='article_detail'),
    path('category/<str:category_name>/', article_list_by_category, name='article_list_by_category'),
    path('add/article',addArticle,name='addArticle'),
        path('article/<int:article_id>/pdf/', generate_pdf, name='generate_pdf'),
        path('article/<int:pk>/edit/', EditArticleView.as_view(), name='edit_article'),
    path('article/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
   path('profile/update/', UserProfileUpdateView.as_view(), name='update_profile'),
   path('contact-us/', contact_us, name='contact_us'),
   path('about_us',about,name = 'about')



]
urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)