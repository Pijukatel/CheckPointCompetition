from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404


class SelfForUser:
    """Returns user object for logged user."""

    def get_object(self):
        return self.request.user


class NoEditForConfirmed:
    """There is no edit view for confirmed object."""
    url = '../'

    def get(self, request, *args, **kwargs):
        if self.get_object().confirmed:
            return HttpResponsePermanentRedirect(self.url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_object().confirmed:
            return HttpResponsePermanentRedirect(self.url)
        return super().post(request, *args, **kwargs)


class GetPoint:
    def get_object(self, queryset=None):
        """Get object by it's name and owner."""
        return get_object_or_404(self.model,
                                 team__name=self.kwargs.get('team'),
                                 checkpoint_id=self.kwargs.get('checkpoint'))
