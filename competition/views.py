from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from competition.forms import AddMembersForm, ConfirmPhoto
from competition.models import Membership, Team, Point
from competition.utils import only_team_member
from competition.views_custom_mixins import SelfForUser, NoEditForConfirmed, GetPoint
from competition.views_generic import ConfirmationView


def home(request):
    """Entry point."""
    return render(request, "competition/home.html")


class TeamPhotoConfirmationView(ConfirmationView):
    model = Team
    template_name = "competition/team_photo_confirmation.html"
    template_name_when_nothing_to_check = "competition/team_photo_confirmation_empty.html"
    form_class = ConfirmPhoto

    def get_success_url(self):
        return reverse_lazy("team", kwargs={'pk': self.checked_object.name})

class PointPhotoConfirmationView(ConfirmationView):
    model = Point
    template_name = "competition/point_photo_confirmation.html"
    template_name_when_nothing_to_check = "competition/team_photo_confirmation_empty.html"
    form_class = ConfirmPhoto

    def get_success_url(self):
        return reverse_lazy("point", kwargs={"team": self.checked_object.team.name,
                                             "checkpoint": self.checked_object.checkpoint.name})

    def get_context_data(self, **kwargs):
        """Adding photo to decide if it is confirmed or not."""
        if not self.extra_context:
            self.extra_context = {}
        self.extra_context.update({"team_photo": self.checked_object.team.photo,
                                   "checkpoint_photo": self.checked_object.checkpoint.photo})
        return super().get_context_data(**kwargs)


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


@only_team_member
@login_required
def add_team_member(request, pk):
    """Only existing members of team can add team members."""
    if Team.objects.get(name=pk).confirmed:
        return HttpResponsePermanentRedirect("../")
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


@method_decorator(only_team_member, name="post")
@method_decorator(only_team_member, name="get")
class TeamUpdate(LoginRequiredMixin, NoEditForConfirmed, UpdateView):
    model = Team
    template_name = "competition/team_update.html"
    fields = ["photo"]


@method_decorator(only_team_member, name="post")
@method_decorator(only_team_member, name="get")
class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "competition/team_delete.html"
    success_url = reverse_lazy("home")


@method_decorator(only_team_member, name="post")
@method_decorator(only_team_member, name="get")
class PointUpdate(GetPoint, NoEditForConfirmed, UpdateView):
    model = Point
    fields = ["photo"]


class PointDetail(GetPoint, DetailView):
    model = Point

    def get_context_data(self, **kwargs):
        """Adding team members info to extra context."""
        if not self.extra_context:
            self.extra_context = {}
        team_photo = self.object.team.photo
        checkpoint_photo = self.object.checkpoint.photo
        self.extra_context.update({"team_photo": team_photo, "checkpoint_photo": checkpoint_photo, })

        return super().get_context_data(**kwargs)


class PointList(ListView):
    model = Point

    def get(self, request, *args, **kwargs):
        """Adding team members info to extra context."""
        self.queryset = Point.objects.filter(team=kwargs["team"])
        return super().get(request, *args, **kwargs)