from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import DetailView

from .views import home, RegisterUser, login_page, User_Page

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/user/', User_Page.as_view(), name='user'),]
