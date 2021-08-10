import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G



@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_confirm_success_redirect_template(client_with_logged_user1):
    # TODO: test with client with staff rights only
    response = client_with_logged_user1.post("/team/photo-confirm/",
                                             {"Confirm photo": "Submit Query"},
                                             follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_detail.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_confirm_template(client_with_logged_user1):
    # TODO: test with client with staff rights only
    response = client_with_logged_user1.get("/team/photo-confirm/", follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_photo_confirmation.html']))

def test_parameters_for_confirm_team_and_point():
    assert False

def test_confirm_refused_explanation():
    assert False

def test_empty_confirm_queue():
    assert False


def test_confirm_top_of_queue():
    assert False


def test_confirm_moves_to_bottom_queue():
    assert False

def test_confirmed():
    assert False