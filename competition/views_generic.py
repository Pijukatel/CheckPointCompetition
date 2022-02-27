from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, RedirectView

from competition.utils import staff_member_required_message


@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="get")
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="post")
class ConfirmationView(UpdateView):
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


@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="get")
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="post")
class RedirectToTopOfConfirmationQueue(RedirectView):
    model = None
    template_name_when_nothing_to_check = "competition/photo_confirmation_empty.html"

    def get_redirect_url(self, *args, **kwargs):
        objects_to_check = self.model.objects.filter(confirmed=False, deny_reason="").exclude(photo='')
        if objects_to_check.exists():
            self.checked_object = objects_to_check.earliest('confirmation_date')
            self.checked_object.save()
            return redirect(self.checked_object.get_absolute_url() + "photo-confirm/")
        return None

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            return url
        return render(request, self.template_name_when_nothing_to_check)
