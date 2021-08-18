
from ..models import Team, Membership

from django import template

register = template.Library()

@register.simple_tag
def team_of_user(user):
    team = Membership.objects.get(user=user).team
    if team:
        return f"{team.name}"
