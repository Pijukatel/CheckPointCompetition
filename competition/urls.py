from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView

from .models import CheckPoint, Team
from .views import (home, RegisterUser, login_page, UserDetail, UserUpdate, UserDelete, TeamDetail, TeamCreate,
                    leave_team, add_team_member, TeamUpdate)

urlpatterns = [
    path('', home, name='home'),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/user/', UserDetail.as_view(), name='user'),
    path('accounts/users/', ListView.as_view(model=User, template_name='competition/user_list.html'), name='users'),
    path('accounts/user/update/', UserUpdate.as_view(model=User), name='user_update'),
    path('accounts/user/delete/', UserDelete.as_view(), name='user_delete'),
    path('checkpoints/', ListView.as_view(model=CheckPoint, template_name= 'competition/checkpoint_list.html'), name='checkpoints'),
    path('checkpoint/<str:pk>/', DetailView.as_view(model=CheckPoint, template_name= 'competition/checkpoint_detail.html'), name='checkpoint'),
    path('team/create/', TeamCreate.as_view(), name='team_create'),
    path('team/leave/', leave_team, name='leave_team'),
    path('team/<str:pk>/', TeamDetail.as_view(), name='team'),
    path('team/<str:pk>/update/', TeamUpdate.as_view(), name='team_update'),
    path('team/<str:pk>/add_member/', add_team_member, name='add_team_member'),
    ]
