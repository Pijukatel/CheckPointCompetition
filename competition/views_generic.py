from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, RedirectView

from competition.forms import ConfirmPhoto
from competition.models import Team
from competition.utils import staff_member_required_message


@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="get")
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="post")
class ConfirmationView(UpdateView):
    # TODO UpdateView with custom model and template and form
    model = None
    template_name = None
    template_name_when_nothing_to_check = None
    form_class = None

    def get_object(self, *args, **kwargs):
        objects = self.model.get_objects_to_confirm(**self.kwargs)
        if objects.exists():
            return objects.first()
        raise Http404("No object matching query.")

    def get_context_data(self, **kwargs):
        """Adding photo to decide if it is confirmed or not."""
        if not self.extra_context:
            self.extra_context = {}
        self.extra_context.update({"photo": self.object.photo})
        return super().get_context_data(**kwargs)


class RedirectToTopOfConfirmationQueue(RedirectView):
    model = None

    def get_redirect_url(self, *args, **kwargs):
        url = None
        objects_to_check = self.model.objects.filter(confirmed=False).exclude(photo='')
        if objects_to_check.exists():
            self.checked_object = objects_to_check.earliest('confirmation_date')
            self.checked_object.save()

        return url


'''
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="get")
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="post")
class ConfirmationView(UpdateView):
    # TODO UpdateView with custom model and template and form
    model = None
    template_name = None
    template_name_when_nothing_to_check = None
    form_class = None

    def __init__(self, **kwargs):
        self._get_object()
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse_lazy("team", kwargs={'pk': self.checked_object.name})

    def get_context_data(self, **kwargs):
        """Adding photo to decide if it is confirmed or not."""
        if not self.extra_context:
            self.extra_context = {}
        self.extra_context.update({"photo": self.checked_object.photo})
        return super().get_context_data(**kwargs)

    def get_object(self, **kwargs):
        return self.checked_object

    def _get_object(self):
        """Get oldest object and save it to renew confirmation_date (put to the end of queue).

        This is done to imitate reverse queue with least amount of effort. Parallel users could be confirming photos
        at the same time. Each time one user asks for new photo to confirm it, it is given and moved to the end of the
        queue by changing it's confirmation date.
        """
        objects_to_check = self.model.objects.filter(confirmed=False).exclude(photo='')
        if objects_to_check.exists():
            self.checked_object = objects_to_check.earliest('confirmation_date')
            self.checked_object.save()

    def _anything_to_check(self):
        if hasattr(self, "checked_object"):
            return True
        return False

    def get(self, request, *args, **kwargs):
        """Handle GET requests only if there is object to check, otherwise redirect."""
        if self._anything_to_check():
            return super().get(request, *args, **kwargs)
        return render(request, self.template_name_when_nothing_to_check)

    def post(self, request, *args, **kwargs):
        """Handle POST requests only if there is object to check, otherwise redirect."""
        if self._anything_to_check():
            return super().post(request, *args, **kwargs)
        return render(request, self.template_name_when_nothing_to_check)
'''
