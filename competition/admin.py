from django.contrib import admin
from .models import CheckPoint


@admin.register(CheckPoint)
class AdminCheckpoint(admin.ModelAdmin):
    """Admin view for Package."""
