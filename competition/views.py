import json
from datetime import datetime

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
from django.contrib.messages.views import SuccessMessageMixin

from competition.forms import AddMembersForm, ConfirmPhoto, PointPhotoForm, CreateInvitationForm
from competition.models import Membership, Team, Point, CheckPoint, UserPosition, Invitation
from competition.score_board import TeamWithScore, get_teams_order
from competition.utils import only_team_member, get_existing_team_if_confirmed, only_non_team_member
from competition.views_custom_mixins import SelfForUser, NoEditForConfirmed, GetPoint
from competition.views_generic import ConfirmationView
from django.views.decorators.clickjacking import xframe_options_sameorigin


def home(request):
    """Entry point."""
    return render(request, "competition/home.html")


@xframe_options_sameorigin
def base_map_view(request):
    return render(request, "competition/components/map_base.html")

class TeamPhotoConfirmationView(ConfirmationView):
    model = Team
    template_name = "competition/team_photo_confirmation.html"
    form_class = ConfirmPhoto


class PointPhotoConfirmationView(ConfirmationView):
    model = Point
    template_name = "competition/point_photo_confirmation.html"
    form_class = ConfirmPhoto

    def get_context_data(self, **kwargs):
        """Adding photo to decide if it is confirmed or not."""
        if not self.extra_context:
            self.extra_context = {}
        self.extra_context.update({"team_photo": self.object.team.photo,
                                   "checkpoint_photo": self.object.checkpoint.photo})
        return super().get_context_data(**kwargs)


@login_required
def leave_team(request):
    """Leave team and redirect to same page."""
    membership = Membership.objects.get(user=request.user)
    team = membership.team
    # Not possible to leave confirmed team.
    if team.confirmed:
        return HttpResponseRedirect(reverse("user"))

    # Remove membership
    membership.team = None
    membership.save()

    # Delete empty team
    if not (Membership.objects.filter(team=team)):
        team.delete()

    return HttpResponseRedirect(reverse("user"))


@only_team_member
@login_required
def invite_member(request, pk):
    """Only existing members of team can add team members."""
    if Team.objects.get(name=pk).confirmed:
        return HttpResponsePermanentRedirect("../")
    form = CreateInvitationForm(by_user=request.user)
    if request.method == "POST":
        form = AddMembersForm(request.POST)
        if form.is_valid():
            Invitation.objects.create(user_id=form.cleaned_data["user"], team_id=pk)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 f"User {User.objects.get(id=form.cleaned_data['user']).username} was invited. User's can confirm or deny invitation.")
            return redirect(reverse('team', args=[pk]))
        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "competition/team_invite_member.html", context)

@only_team_member
@login_required
def delete_inivation(request, pk, invited_user):
    """Delete sent invitation."""
    if Team.objects.get(name=pk).confirmed:
        return HttpResponsePermanentRedirect("../")
    Invitation.objects.get(team_id=pk, user_id=User.objects.get(username=invited_user)).delete()
    messages.add_message(request,
                         messages.SUCCESS,
                         f"Invitation to {invited_user} was withdrawn.")
    return redirect(reverse('team', args=[pk]))

@login_required
def refuse_invitation(request, pk):
    """Refuse sent invitation."""
    if Team.objects.get(name=pk).confirmed:
        return HttpResponsePermanentRedirect("../")
    Invitation.objects.get(team_id=pk, user=request.user).delete()
    return HttpResponsePermanentRedirect("/")

@login_required
def accept_invitation(request, pk):
    """Accept sent invitation."""
    if Team.objects.get(name=pk).confirmed:
        messages.add_message(request,
                             messages.SUCCESS,
                             f"Team was already confirmed. Can't join!")
        return HttpResponsePermanentRedirect("../")
    membership = Membership.objects.get(user=request.user)
    membership.team_id = pk
    membership.save()
    messages.add_message(request,
                         messages.SUCCESS,
                         f"You have joined the team: {pk}.")
    return HttpResponsePermanentRedirect("/")

class RegisterUser(SuccessMessageMixin, CreateView):
    """Register view."""
    template_name = "competition/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = "{username} user created, you can now login."

    def get_success_message(self, cleaned_data):
        return self.success_message.format(username=self.object.username)


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


def logout_link(request):
    """Handle logout."""
    logout(request)
    return redirect('login')


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
        invited_members = [User.objects.get(username=team.user) for team in Invitation.objects.filter(team=self.object)]
        self.extra_context.update({"members": members, "invited_members": invited_members})

        return super().get_context_data(**kwargs)


class TeamList(ListView):
    template_name = "competition/team_list.html"

    def get_queryset(self):
        return get_teams_order()


class UserUpdate(LoginRequiredMixin, SelfForUser, UpdateView):
    fields = ["first_name"]
    template_name = "competition/user_update.html"
    success_url = reverse_lazy("user")


class UserDelete(LoginRequiredMixin, SelfForUser, DeleteView):
    template_name = "competition/user_delete.html"
    success_url = reverse_lazy("home")


@method_decorator(login_required, name="post")
@method_decorator(login_required, name="get")
@method_decorator(only_non_team_member, name="post")
@method_decorator(only_non_team_member, name="get")
class TeamCreate(SuccessMessageMixin, CreateView):
    model = Team
    template_name = "competition/team_create.html"
    fields = ["name"]
    success_message = "{name} team created, you can now invite others to the team."

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=self.object.name)

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

    def form_valid(self, form):
        """Delete deny reason when updated."""
        self.object.deny_reason = ""
        return super().form_valid(form)


@method_decorator(only_team_member, name="post")
@method_decorator(only_team_member, name="get")
class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "competition/team_delete.html"
    success_url = reverse_lazy("home")


def checkpoint_view(request, *args, **kwargs):
    """Non standard view that shows checkpoint details and for users that are members of team it also shows
    point details with option to edit Point photo if not confirmed yet."""
    checkpoint = CheckPoint.objects.get(name=kwargs['pk'])
    context = {}
    context.update({"checkpoint": checkpoint})
    if request.user.is_authenticated:
        if team_object := get_existing_team_if_confirmed(user=request.user):
            point = Point.objects.get(team=team_object, checkpoint_id=kwargs['pk'])
            if request.POST:
                form = PointPhotoForm(request.POST, request.FILES, instance=point)
            else:
                form = PointPhotoForm(None)
            if form.is_valid() and not point.confirmed:
                form.save()
                point.deny_reason = ""  # Reset deny reason with update.
                point.visit_date = pytz.UTC.localize(datetime.now())
                point.save()
            context.update({"point_photo": point.photo, "deny_reason": point.deny_reason,
                            "point_confirmed": point.confirmed, "form": form, "team": team_object.name})
            return render(request, "competition/components/checkpoint_detail_confirmed_team.html", context)
    return render(request, "competition/checkpoint_detail.html", context)


class CheckpointList(ListView):
    model = CheckPoint
    template_name = "competition/checkpoint_list.html"

    def get_context_data(self, **kwargs):
        """Adding team members info to extra context."""
        if not self.extra_context:
            self.extra_context = {}
        if self.request.user.is_authenticated:
            if team_object := get_existing_team_if_confirmed(user=self.request.user):
                self.template_name = "competition/checkpoint_list_confirmed_team.html"
                points = Point.objects.filter(team=team_object).order_by('checkpoint_id')
                self.extra_context.update({"team_object": team_object, "checkpoints": self.object_list})
                self.object_list = zip(self.object_list, points)
        return super().get_context_data(**kwargs)


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
