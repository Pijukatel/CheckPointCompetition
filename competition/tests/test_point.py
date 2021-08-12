import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G


def test_only_team_members_with_confirmed_team_can_create_point():
    assert False


def test_only_team_members_with_confirmed_team_can_update_point():
    assert False



@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_view_point(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/point/{G.team1_name}/{G.checkpoint1_name}/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "point_detail.html"]))



def test_list_point():
    assert False


def test_templates_from_components():
    assert False