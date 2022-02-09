import pytest

from ..models import Team, User, Membership, CheckPoint, Point
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
def load_registered_user3():
    user = User(username=G.user3_name, password=make_password(G.user3_password))
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
def load_team3():
    team = Team(name=G.team3_name, photo=f"teams/{G.test_image_name}")
    team.save()
    # To fool auto-updated time.
    Team.objects.filter(name=G.team3_name).update(confirmation_date=G.team3_photo_confirmation_date)
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
def load_registered_user3_with_team3(load_registered_user3, load_team3):
    team = load_team3
    membership = Membership(user_id=load_registered_user3.id, team_id=team.name)
    membership.save()
    yield load_registered_user3, team, membership
    membership.delete()


@pytest.fixture
def load_registered_user2_with_team2_no_photo(load_registered_user2_with_team2):
    user, team, membership = load_registered_user2_with_team2
    team.photo = ""
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


@pytest.fixture
def load_checkpoint1():
    checkpoint = CheckPoint(name=G.checkpoint1_name, description=G.checkpoint1_description, gps_lon=G.checkpoint1_lon,
                            gps_lat=G.checkpoint1_lat, photo=f"checkpoint/{G.checkpoint1_image_name}")
    checkpoint.save()
    yield checkpoint
    checkpoint.delete()


@pytest.fixture
def load_checkpoint2():
    checkpoint = CheckPoint(name=G.checkpoint2_name, description=G.checkpoint2_description, gps_lon=G.checkpoint2_lon,
                            gps_lat=G.checkpoint2_lat, photo=f"checkpoint/{G.checkpoint2_image_name}")
    checkpoint.save()
    yield checkpoint
    checkpoint.delete()


@pytest.fixture
def load_checkpoint3():
    checkpoint = CheckPoint(name=G.checkpoint3_name, description=G.checkpoint3_description, gps_lon=G.checkpoint3_lon,
                            gps_lat=G.checkpoint3_lat, photo=f"checkpoint/{G.checkpoint3_image_name}")
    checkpoint.save()
    yield checkpoint
    checkpoint.delete()


@pytest.fixture
def load_point1(load_team1, load_checkpoint1):
    team = load_team1
    checkpoint = load_checkpoint1
    point = Point(team=team, checkpoint=checkpoint, photo=f"point/{G.point1_image_name}")
    point.save()
    # To fool auto-updated time.
    Point.objects.filter(id=point.id).update(confirmation_date=G.point1_photo_confirmation_date)
    yield point
    point.delete()


@pytest.fixture
def load_point1_no_photo(load_point1):
    point = load_point1
    point.photo = ""
    point.save()
    # To fool auto-updated time.
    Point.objects.filter(id=point.id).update(confirmation_date=G.point1_photo_confirmation_date)


@pytest.fixture
def load_point1_confirmed(load_point1):
    point = load_point1
    point.confirmed = True
    point.save()
    # To fool auto-updated time.
    Point.objects.filter(id=point.id).update(confirmation_date=G.point1_photo_confirmation_date)


@pytest.fixture
def load_point2(load_team1, load_checkpoint2):
    team = load_team1
    checkpoint = load_checkpoint2
    point = Point(team=team, checkpoint=checkpoint, photo=f"point/{G.point2_image_name}")
    point.save()
    # To fool auto-updated time.
    Point.objects.filter(id=point.id).update(confirmation_date=G.point2_photo_confirmation_date)
    yield point
    point.delete()


@pytest.fixture
def load_point3(load_team2, load_checkpoint2):
    team = load_team2
    checkpoint = load_checkpoint2
    point = Point(team=team, checkpoint=checkpoint, photo=f"point/{G.point3_image_name}")
    point.save()
    # To fool auto-updated time.
    Point.objects.filter(id=point.id).update(confirmation_date=G.point3_photo_confirmation_date)
    yield point
    point.delete()


@pytest.fixture
def load_confirmed_teams_1_2_3_and_checkpoints_1_2_3(load_team1, load_team2, load_team3,
                                                     load_checkpoint1, load_checkpoint2, load_checkpoint3):
    teams = (load_team1, load_team2, load_team3)
    for team in teams:
        team.confirmed = True
        team.save()
    checkpoints = [load_checkpoint1, load_checkpoint2, load_checkpoint3]
    yield teams, checkpoints
    for point in Point.objects.all():
        point.delete()
