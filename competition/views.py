from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from competition.views_custom_mixins import SelfForUser
from competition.models import Membership


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


class UserPage(LoginRequiredMixin, SelfForUser, DetailView):
    template_name = 'competition/user_detail.html'

    def get_context_data(self, **kwargs):
        """Adding user's team membership info to context extra data."""
        if not self.extra_context:
            self.extra_context = {}
        self.extra_context.update({'team': Membership.objects.get(user=self.request.user).team})

        return super().get_context_data(**kwargs)


class UserUpdate(LoginRequiredMixin, SelfForUser, UpdateView):
    fields = ['first_name']
    template_name = 'competition/user_update.html'
    success_url = reverse_lazy('user')


class UserDelete(LoginRequiredMixin, SelfForUser, DeleteView):
    template_name = 'competition/user_delete.html'
    success_url = reverse_lazy('home')
