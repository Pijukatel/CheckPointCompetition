from django import forms

from .models import Membership, Team


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
