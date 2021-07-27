from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


def home(request):
    """Entry point."""
    return render(request, 'competition/home.html')


class RegisterUser(CreateView):
    """Register view."""
    template_name = 'competition/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')


'''
def login_page(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        messages.info(request, 'Username or password is incorrect.')
        return render(request, 'PackageDB/login.html', {'form': LoginForm})

    elif request.method == 'GET':
        return render(request, 'PackageDB/login.html', {'form': LoginForm})
'''
