import pytest
from django.contrib.auth.models import User

from .globals_for_tests import G
from ..models import Team
from ..templatetags.competition_template_utils import team_of_user


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_of_user():
    user = User.objects.get(username=G.user1_name)
    team = Team.objects.get(name=G.team1_name)
    assert team.name == team_of_user(user)
