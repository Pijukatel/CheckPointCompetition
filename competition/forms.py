from django import forms
from .models import Membership
from django import forms


class ConfirmPhoto(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

    def clean(self):
        if 'newsletter_sub' in self.data:
            pass
        elif 'newsletter_unsub' in self.data:
            pass



class AddMembersForm(forms.Form):
    user = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = Membership.objects.filter(team=None)
        self.fields['user'].choices = [(option.user.id, option.user.username) for option in options]
