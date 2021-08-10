from django.contrib import admin
from .models import CheckPoint, Membership, Point, Team


@admin.register(CheckPoint)
class AdminCheckpoint(admin.ModelAdmin):
    pass


@admin.register(Membership)
class AdminMembership(admin.ModelAdmin):
    pass


@admin.register(Point)
class AdminPoint(admin.ModelAdmin):
    pass


@admin.register(Team)
class AdminTeam(admin.ModelAdmin):
    pass
