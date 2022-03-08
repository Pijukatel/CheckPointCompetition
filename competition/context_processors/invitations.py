from django.contrib import messages

from competition.models import Membership, Invitation


def add_invitations(request):
    if not request.path.startswith("/api") and request.user.is_authenticated and not Membership.objects.get(user=request.user).team:
        return {"invitations": tuple(invitation.team.name for invitation in Invitation.objects.filter(user=request.user))}
    else:
        return {"invitations": tuple()}


