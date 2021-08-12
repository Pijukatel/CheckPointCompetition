import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from ..models import Team, Point, CheckPoint


def test_only_team_members_with_confirmed_team_can_update_point():
    assert False


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_view_point_template(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/point/{G.team1_name}/{G.checkpoint1_name}/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "point_detail.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_by_team_member_template(client_with_logged_user1):
    # TODO: Only team member can update photo
    response = client_with_logged_user1.get(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "point_form.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_post_by_team_member_template(client_with_logged_user1):
    with open('competition/fixtures/test_image.jpg', 'rb') as fp:
        response = client_with_logged_user1.post(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/",
                                                 {"Upload photo": "Photo.jpg",
                                                  "photo": fp},
                                                 follow=True)
    assert False
    # Does not update picture TODO: FIX


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_by_non_team_member_template(client_with_logged_user2):
    response = client_with_logged_user2.get(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_post_by_non_team_member_template(client_with_logged_user2):
    response = client_with_logged_user2.post(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/",
                                             {"Upload photo": "Photo.jpg"},
                                             follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_by_non_team_member_message(client_with_logged_user2):
    response = client_with_logged_user2.get(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/", follow=True)
    assert bytes("Only team members can do that. Log in as member of that team.",
                 encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_post_by_non_team_member_message(client_with_logged_user2):
    response = client_with_logged_user2.post(f"/point/{G.team1_name}/{G.checkpoint1_name}/update/",
                                             {"Upload photo": "Photo.jpg"},
                                             follow=True)
    assert bytes("Only team members can do that. Log in as member of that team.",
                 encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_auto_create_points_for_confirmed_team():
    """Once team is confirmed, points are automatically created
     for each checkpoint and this confirmed team."""

    team = Team.objects.get(name=G.team1_name)
    team.confirmed = True
    team.save()
    checkpoints = CheckPoint.objects.all()
    for checkpoint in checkpoints:
        assert Point.objects.filter(team=team, checkpoint=checkpoint).exists()
    assert len(checkpoints) == len(Point.objects.all())


def test_auto_delete_points_when_team_is_deleted():
    assert False


def test_list_point():
    assert False


def test_templates_from_components():
    assert False


def test_confirmed_point_cant_be_updated():
    assert False
