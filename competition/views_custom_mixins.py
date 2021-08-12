from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from competition.models import Team, Membership


class SelfForUser:
    """Returns user object for logged user."""

    def get_object(self):
        return self.request.user


class OnlyTeamMemberMixin:
    """Allow view only for user that is team member."""

    def dispatch(self, request, *args, **kwargs):
        team = Team.objects.get(name=kwargs['pk'])
        membership = Membership.objects.filter(user=request.user, team=team).exists()
        if membership:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class NoEditForConfirmed:
    """There is edit view for confirmed object."""
    url = '../'

    def get(self, request, *args, **kwargs):
        if Team.objects.get(name=kwargs['pk']).confirmed:
            return HttpResponsePermanentRedirect(self.url)
        return super().get(request, *args, **kwargs)


class GetPoint:
    def get_object(self, queryset=None):
        """Get object by it's name and owner."""
        return get_object_or_404(self.model,
                                 team__name=self.kwargs.get('team'),
                                 checkpoint_id=self.kwargs.get('checkpoint'))
