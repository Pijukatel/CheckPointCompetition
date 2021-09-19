from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from competition.models import Team, Membership
from competition.templatetags.competition_template_utils import team_of_user


def user_is_not_staff(request):
    return not(request.user.is_active and request.user.is_staff)


def message_decorator_factory(message_level, message_content, condition_function):
    def message_decorator(func):
        """Decorator for adding custom messages to functions with requests."""

        def _add_message(request, *args, **kwargs):
            if condition_function(request):
                messages.add_message(request, message_level, message_content)
            return func(request, *args, **kwargs)

        return _add_message

    return message_decorator


staff_member_required_message = message_decorator_factory(
    messages.INFO,
    "Only staff members can confirm photos. Log in as staff member.",
    user_is_not_staff)


def only_team_member(func):
    def _only_team_member(request, *args, **kwargs):
        """Only team members can continue.
        Redirect others to login and give explanation message."""

        if "team" in kwargs:
            team = Team.objects.get(name=kwargs["team"])
        else:
            team = Team.objects.get(name=kwargs["pk"])

        membership = Membership.objects.filter(user=request.user, team=team)

        if membership.exists():
            return func(request, *args, **kwargs)

        messages.add_message(request,
                             messages.INFO,
                             "Only team members can do that. Log in as member of that team.")
        return HttpResponseRedirect(reverse("login"))

    return _only_team_member


def get_existing_team_if_confirmed(user):
    """If user is member of confirmed team, return team object. Otherwise None."""
    team_object = Team.objects.filter(name=team_of_user(user))
    if team_object.exists():
        team_object = team_object.first()
        if team_object.confirmed:
            return team_object
    return None