import pytest
from django.contrib.auth.models import User

from competition.utils import get_existing_team_if_confirmed
from .globals_for_tests import G
from ..models import Team


@pytest.mark.usefixtures("load_registered_user1")
@pytest.mark.django_db
def test_get_existing_team_if_confirmed_user_without_team():
    assert get_existing_team_if_confirmed(User.objects.get(username=G.user1_name)) is None


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_get_existing_team_if_confirmed_user_in_unconfirmed_team():
    assert get_existing_team_if_confirmed(User.objects.get(username=G.user1_name)) is None


@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_get_existing_team_if_confirmed_user_in_confirmed_team():
    assert get_existing_team_if_confirmed(User.objects.get(username=G.user1_name)) == Team.objects.get(name=G.team1_name)
