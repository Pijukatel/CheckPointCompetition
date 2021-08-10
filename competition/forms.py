from django import forms
from .models import Membership


class AddMembersForm(forms.Form):
    user = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = Membership.objects.filter(team=None)
        self.fields['user'].choices = [(option.user.id, option.user.username) for option in options]
