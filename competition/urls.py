from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import ListView

from .views import home, RegisterUser, login_page, UserPage, UserUpdate, UserDelete

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/user/', UserPage.as_view(), name='user'),
    path('accounts/users/', ListView.as_view(model=User, template_name='competition/user_list.html'), name='users'),
    path('accounts/user/update/', UserUpdate.as_view(model=User), name='user_update'),
    path('accounts/user/delete/', UserDelete.as_view(), name='user_delete')]
