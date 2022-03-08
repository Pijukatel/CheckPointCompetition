from django import forms
from django.db.models import Q

from .models import Membership, Team, Point, Invitation


class PointPhotoForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ["photo"]


class ConfirmPhoto(forms.ModelForm):

    def clean(self):
        if self.data["Confirm photo"] == "True":
            self.cleaned_data["confirmed"] = True
            self.cleaned_data["deny_reason"] = ""

    class Meta:
        model = Team
        fields = ["deny_reason", "confirmed"]
        widgets = {
            "confirmed": forms.HiddenInput(),
        }


class AddMembersForm(forms.Form):
    user = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = Membership.objects.filter(team=None)
        self.fields['user'].choices = [(option.user.id, option.user.username) for option in options]

class CreateInvitationForm(forms.Form):
    user = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        by_user = kwargs.pop("by_user")
        super().__init__(*args, **kwargs)
        team = Membership.objects.get(user=by_user).team
        users_without_team = {(membership.user.id, membership.user.username) for membership in Membership.objects.filter(team=None)}
        already_invited_users = {(membership.user.id, membership.user.username) for membership in Invitation.objects.filter(team=team)}
        self.fields['user'].choices = users_without_team - already_invited_users