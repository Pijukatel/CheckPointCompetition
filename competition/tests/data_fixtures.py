import pytest

from ..models import Team, User, Membership
from .globals_for_tests import G
from django.contrib.auth.hashers import make_password


@pytest.fixture
def load_registered_user1():
    user = User(username=G.user1_name, password=make_password(G.user1_password))
    user.save()
    yield user
    user.delete()


@pytest.fixture
def load_registered_user2():
    user = User(username=G.user2_name, password=make_password(G.user2_password))
    user.save()
    yield user
    user.delete()

@pytest.fixture
def load_registered_user_with_is_staff():
    user = User(username=G.user_staff_name, password=make_password(G.user_staff_password), is_staff=True)
    user.save()
    yield user
    user.delete()


@pytest.fixture
def load_team1():
    team = Team(name=G.team1_name, photo=f"teams/{G.test_image_name}")
    team.save()
    # To fool auto-updated time.
    Team.objects.filter(name=G.team1_name).update(confirmation_date=G.team1_photo_confirmation_date)
    yield team
    team.delete()


@pytest.fixture
def load_team2():
    team = Team(name=G.team2_name, photo=f"teams/{G.test_image_name}")
    team.save()
    # To fool auto-updated time.
    Team.objects.filter(name=G.team2_name).update(confirmation_date=G.team2_photo_confirmation_date)
    yield team
    team.delete()


@pytest.fixture
def load_registered_user1_with_team1(load_registered_user1, load_team1):
    team = load_team1
    membership = Membership(user_id=load_registered_user1.id, team_id=team.name)
    membership.save()
    yield load_registered_user1, team, membership
    membership.delete()

@pytest.fixture
def load_registered_user2_with_team2(load_registered_user2, load_team2):
    team = load_team2
    membership = Membership(user_id=load_registered_user2.id, team_id=team.name)
    membership.save()
    yield load_registered_user2, team, membership
    membership.delete()

@pytest.fixture
def load_registered_user2_with_team2_no_photo(load_registered_user2_with_team2):
    user, team, membership = load_registered_user2_with_team2
    team.photo=""
    team.save()

@pytest.fixture
def load_registered_users_1_2_with_team1(load_registered_user1, load_registered_user2, load_team1):
    team = load_team1
    memberships = (Membership(user_id=load_registered_user1.id, team_id=team.name),
                   Membership(user_id=load_registered_user2.id, team_id=team.name))
    for membership in memberships:
        membership.save()
    yield load_registered_user1, load_registered_user2, team, memberships
    for membership in memberships:
        membership.delete()


@pytest.fixture
def load_registered_user1_with_confirmed_team1(load_registered_user1_with_team1):
    user, team, membership = load_registered_user1_with_team1
    team.confirmed = True
    team.save()


