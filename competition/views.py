from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from competition.forms import AddMembersForm, ConfirmPhoto
from competition.models import Membership, Team
from competition.utils import staff_member_required_message
from competition.views_custom_mixins import SelfForUser, OnlyTeamMemberMixin, NoEditForConfirmed


def home(request):
    """Entry point."""
    return render(request, "competition/home.html")


@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="get")
@method_decorator([staff_member_required_message, staff_member_required(login_url="login")], name="post")
class ConfirmationView(UpdateView):
    # TODO UpdateView with custom model and template and form
    model = Team
    template_name = "competition/team_photo_confirmation.html"
    template_name_when_nothing_to_check = "competition/team_photo_confirmation_empty.html"
    form_class = ConfirmPhoto

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


@login_required
def leave_team(request):
    """Leave team and redirect to same page."""
    membership = Membership.objects.get(user=request.user)
    team = membership.team

    # Remove membership
    membership.team = None
    membership.save()

    # Delete empty team
    if not (Membership.objects.filter(team=team)):
        team.delete()

    return HttpResponseRedirect(reverse("user"))


@login_required
def add_team_member(request, pk):
    """Only existing members of team can add team members."""
    if Membership.objects.filter(user=request.user, team__name=pk):
        pass
    else:
        return HttpResponseForbidden()

    form = AddMembersForm()
    if request.method == "POST":
        form = AddMembersForm(request.POST)
        if form.is_valid():
            membership = Membership.objects.get(user=form.cleaned_data["user"])
            membership.team = Team.objects.get(name=pk)
            membership.save()
            return redirect(reverse('team', args=[pk]))
        else:
            print(form.errors)

    context = {"form": form}
    return render(request, "competition/team_add_member.html", context)


class RegisterUser(CreateView):
    """Register view."""
    template_name = "competition/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def login_page(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("user")

        messages.info(request, "Username or password is incorrect.")
        return render(request, "competition/login.html", {"form": AuthenticationForm})

    elif request.method == 'GET':
        return render(request, "competition/login.html", {"form": AuthenticationForm})


class UserDetail(LoginRequiredMixin, SelfForUser, DetailView):
    template_name = "competition/user_detail.html"

    def get_context_data(self, **kwargs):
        """Adding user's team membership info to context extra data."""
        if not self.extra_context:
            self.extra_context = {}
        # Some users are not members of any team yet.
        team_name = getattr(Membership.objects.get(user=self.request.user).team, "name", None)
        self.extra_context.update({"team": team_name})

        return super().get_context_data(**kwargs)


class TeamDetail(DetailView):
    template_name = "competition/team_detail.html"
    model = Team

    def get_context_data(self, **kwargs):
        """Adding team members info to extra context."""
        if not self.extra_context:
            self.extra_context = {}
        members = [User.objects.get(username=team.user) for team in Membership.objects.filter(team=self.object)]
        self.extra_context.update({"members": members})

        return super().get_context_data(**kwargs)


class UserUpdate(LoginRequiredMixin, SelfForUser, UpdateView):
    fields = ["first_name"]
    template_name = "competition/user_update.html"
    success_url = reverse_lazy("user")


class UserDelete(LoginRequiredMixin, SelfForUser, DeleteView):
    template_name = "competition/user_delete.html"
    success_url = reverse_lazy("home")


class TeamCreate(CreateView):
    model = Team
    template_name = "competition/team_create.html"
    fields = ["name"]

    def form_valid(self, form):
        """Assign currently signed user to join created team."""
        response = super().form_valid(form)
        membership = Membership.objects.get(user=self.request.user)
        membership.team = form.instance
        membership.save()
        return response


class TeamUpdate(LoginRequiredMixin, OnlyTeamMemberMixin, NoEditForConfirmed, UpdateView):
    model = Team
    template_name = 'competition/team_update.html'
    fields = ['photo']


class TeamDelete(LoginRequiredMixin, OnlyTeamMemberMixin, DeleteView):
    model = Team
    template_name = "competition/team_delete.html"
    success_url = reverse_lazy("home")
