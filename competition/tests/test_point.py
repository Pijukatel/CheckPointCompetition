import pytest
from pytest_django.asserts import assertTemplateUsed, assertTemplateNotUsed
from .globals_for_tests import G
from ..models import Team, Point, CheckPoint


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
def test_update_point_post_by_team_member_template(client_with_logged_user1):
    with open("competition/fixtures/test_image.jpg", "rb") as fp:
        response = client_with_logged_user1.post(f"/checkpoint/{G.checkpoint1_name}/",
                                                 {"Upload photo": "Photo.jpg",
                                                  "photo": fp},
                                                 follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/point_form.html"]))
    assert Point.objects.all()[0].photo.name == f"points/{G.test_image_name}"


@pytest.mark.usefixtures("delete_test_image")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_post_deletes_deny_reason(client_with_logged_user1):
    point = Point.objects.all()[0]
    point.deny_reason = ""
    point.save()
    with open("competition/fixtures/test_image.jpg", "rb") as fp:
        response = client_with_logged_user1.post(f"/checkpoint/{G.checkpoint1_name}/",
                                                 {"Upload photo": "Photo.jpg",
                                                  "photo": fp},
                                                 follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/point_form.html"]))
    point.refresh_from_db()
    assert point.photo.name == f"points/{G.test_image_name}"
    assert point.deny_reason == ""


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_confirmed_point_post_by_team_member_template(client_with_logged_user1):
    """No update should be done to confirmed point."""
    point = Point.objects.all()[0]
    point.confirmed = True
    point.save()
    with open("competition/fixtures/test_image.jpg", "rb") as fp:
        response = client_with_logged_user1.post(f"/checkpoint/{G.checkpoint1_name}/",
                                                 {"Upload photo": "Photo.jpg",
                                                  "photo": fp},
                                                 follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assert Point.objects.all()[0].photo.name == f"point/{G.point1_image_name}"


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_confirmed_point_by_team_member_template(client_with_logged_user1):
    """No update should be done to confirmed point."""
    point = Point.objects.all()[0]
    point.confirmed = True
    point.save()
    response = client_with_logged_user1.get(f"/checkpoint/{G.checkpoint1_name}/",
                                            follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assertTemplateNotUsed(response, "/".join([G.APP_NAME, "components/point_form.html"]))


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_update_point_post_by_non_team_member_template(client_with_logged_user2):
    with open("competition/fixtures/test_image.jpg", "rb") as fp:
        response = client_with_logged_user2.post(f"/checkpoint/{G.checkpoint1_name}/",
                                                 {"Upload photo": "Photo.jpg",
                                                  "photo": fp},
                                                 follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_detail.html"]))
    assert Point.objects.all()[0].photo.name == f"point/{G.point1_image_name}"


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
