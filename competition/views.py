from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    """Entry point."""
    return render(request, 'competition/home.html')


class RegisterUser(CreateView):
    """Register view."""
    template_name = 'competition/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def login_page(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('user')

        messages.info(request, 'Username or password is incorrect.')
        return render(request, 'competition/login.html', {'form': AuthenticationForm})

    elif request.method == 'GET':
        return render(request, 'competition/login.html', {'form': AuthenticationForm})


class User_Page(LoginRequiredMixin, DetailView):
    """For user edit and import export of data."""
    template_name = 'competition/user_detail.html'

    def get_object(self):
        return self.request.user

