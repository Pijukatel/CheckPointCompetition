from django.contrib import admin
from django.urls import path

from .views import home, RegisterUser

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register/', RegisterUser.as_view(), name='register')]
