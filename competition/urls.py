from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from .models import CheckPoint
from .views import home, RegisterUser, login_page, UserPage, UserUpdate, UserDelete

urlpatterns = [
    path('', home, name='home'),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/user/', UserPage.as_view(), name='user'),
    path('accounts/users/', ListView.as_view(model=User, template_name='competition/user_list.html'), name='users'),
    path('accounts/user/update/', UserUpdate.as_view(model=User), name='user_update'),
    path('accounts/user/delete/', UserDelete.as_view(), name='user_delete'),
    path('checkpoints', ListView.as_view(model=CheckPoint, template_name= 'competition/checkpoint_list.html'), name='checkpoints'),
    path('checkpoint/<int:pk>/', DetailView.as_view(model=CheckPoint, template_name= 'competition/checkpoint_detail.html'), name='checkpoint')]
