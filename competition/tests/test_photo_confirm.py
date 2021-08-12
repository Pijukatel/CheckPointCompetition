import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from ..models import Team


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_success_redirect_template(client_with_logged_user_staff):
    response = client_with_logged_user_staff.post("/team/photo-confirm/",
                                                  {"Confirm photo": "True"},
                                                  follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_detail.html"]))


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_saves_confirmed(client_with_logged_user_staff):
    client_with_logged_user_staff.post("/team/photo-confirm/",
                                       {"Confirm photo": "True"},
                                       follow=True)
    assert Team.objects.get(name=G.team1_name).confirmed


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_post_non_staff(client_with_logged_user1):
    """Non staff users that manually send confirmation post request should not affect database
     and should be redirected to login."""
    response = client_with_logged_user1.post("/team/photo-confirm/",
                                             {"Confirm photo": "True"},
                                             follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))
    assert Team.objects.get(name=G.team1_name).confirmed is False


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_post_message_for_non_staff_user(client_with_logged_user1):
    response = client_with_logged_user1.post("/team/photo-confirm/",
                                             {"Confirm photo": "True"},
                                             follow=True)
    assert bytes("Only staff members can confirm photos. Log in as staff member.",
                 encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_post_no_message_for_staff_user(client_with_logged_user_staff):
    response = client_with_logged_user_staff.post("/team/photo-confirm/",
                                                  {"Confirm photo": "True"},
                                                  follow=True)
    assert bytes("Only staff members can confirm photos. Log in as staff member.",
                 encoding=response.charset) not in response.content


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_template(client_with_logged_user_staff):
    response = client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_photo_confirmation.html"]))


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_template_for_non_staff_user(client_with_logged_user1):
    response = client_with_logged_user1.get("/team/photo-confirm/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_message_for_non_staff_user(client_with_logged_user1):
    response = client_with_logged_user1.get("/team/photo-confirm/", follow=True)
    assert bytes("Only staff members can confirm photos. Log in as staff member.",
                 encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_no_message_for_staff_user(client_with_logged_user_staff):
    response = client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assert bytes("Only staff members can confirm photos. Log in as staff member.",
                 encoding=response.charset) not in response.content


@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_confirm_template_when_all_confirmed(client_with_logged_user_staff):
    response = client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_photo_confirmation_empty.html"]))


@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.usefixtures("load_registered_user2_with_team2_no_photo")
@pytest.mark.django_db
def test_confirm_template_when_unconfirmed_teams_have_no_photo(client_with_logged_user_staff):
    response = client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_photo_confirmation_empty.html"]))


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.django_db
def test_confirm_top_of_confirm_queue_used(client_with_logged_user_staff):
    # Team1 confirmation date is older and should be on top of queue
    response = client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assert bytes(G.team1_name, encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.django_db
def test_confirm_moves_to_bottom_of_queue(client_with_logged_user_staff):
    # Team1 confirmation date is older and should be on top of queue.
    # After viewing Team1, it will be moved to bottom of queue regardless of confirmation outcome.
    # (Imaginary queue based on datetime object. Bottom is latest, top is oldest.)
    old_date = Team.objects.get(name=G.team1_name).confirmation_date
    client_with_logged_user_staff.get("/team/photo-confirm/", follow=True)
    assert Team.objects.get(name=G.team1_name).confirmation_date > old_date
    assert Team.objects.get(name=G.team1_name).confirmation_date > Team.objects.get(name=G.team2_name).confirmation_date


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_deny_photo_shows_explanation(client_with_logged_user_staff):
    deny_reason = "Some reason."
    response = client_with_logged_user_staff.post("/team/photo-confirm/",
                                                  {"Confirm photo": "False",
                                                   "deny_reason": deny_reason},
                                                  follow=True)
    assert bytes(deny_reason, encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_deny_photo_saves_explanation(client_with_logged_user_staff):
    deny_reason = "Some reason."
    client_with_logged_user_staff.post("/team/photo-confirm/",
                                       {"Confirm photo": "False",
                                        "deny_reason": deny_reason},
                                       follow=True)
    assert Team.objects.get(name=G.team1_name).deny_reason == deny_reason


@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_confirm_photo_do_not_show_explanation(client_with_logged_user_staff):
    """deny_reason is irrelevant when approved"""
    deny_reason = "Some reason."
    response = client_with_logged_user_staff.post("/team/photo-confirm/",
                                                  {"Confirm photo": "True",
                                                   "deny_reason": deny_reason},
                                                  follow=True)
    assert bytes(deny_reason, encoding=response.charset) not in response.content


def test_parameters_for_confirm_team_and_point():
    """Parametrize tests once both the team and point confirmation are implemented."""
    assert False
