from django.shortcuts import render

# Create your views here.


def home(request):
    """Entry point."""
    return render(request, 'competition/home.html')