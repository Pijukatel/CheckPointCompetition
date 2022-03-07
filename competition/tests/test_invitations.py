import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup
from .globals_for_tests import G
from ..models import Invitation, Team


@pytest.mark.usefixtures("load_registered_user4")
@pytest.mark.usefixtures("load_registered_user3")
@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_options_users_without_team(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/team/{G.team1_name}/invite_member/")
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_invite_member.html"]))
    soup = BeautifulSoup(response.content)
    assert {G.user2_name, G.user3_name, G.user4_name} == {option.text for option in soup.select('#id_user option')}


@pytest.mark.usefixtures("load_registered_user4")
@pytest.mark.usefixtures("load_registered_user3")
@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_options_no_team_members(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/team/{G.team1_name}/invite_member/")
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_invite_member.html"]))
    soup = BeautifulSoup(response.content)
    assert {G.user3_name, G.user4_name} == {option.text for option in soup.select('#id_user option')}


@pytest.mark.usefixtures("load_registered_user4")
@pytest.mark.usefixtures("load_registered_user3")
@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_options_exclude_already_invited_to_this_team(client_with_logged_user1):
    # Create invitation to this team (should not be an option to send invite to)
    Invitation.objects.create(team_id=G.team1_name, user=User.objects.get(username=G.user3_name))
    # Create invitation to another team (should still be an option to invite to different team)
    Invitation.objects.create(team_id=G.team2_name, user=User.objects.get(username=G.user4_name))
    response = client_with_logged_user1.get(f"/team/{G.team1_name}/invite_member/")
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_invite_member.html"]))
    soup = BeautifulSoup(response.content)
    assert {G.user4_name} == {option.text for option in soup.select('#id_user option')}


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_only_for_members_annonymous(client):
    response = client.get(f"/team/{G.team1_name}/invite_member/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))
    soup = BeautifulSoup(response.content)
    assert soup.select(".messages li")[0].text == "Only team members can do that. Log in as member of that team."


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_only_for_members_other_team_tries(client_with_logged_user2):
    response = client_with_logged_user2.get(f"/team/{G.team1_name}/invite_member/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))
    soup = BeautifulSoup(response.content)
    assert soup.select(".messages li")[0].text == "Only team members can do that. Log in as member of that team."


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_invitation_only_for_nonconfirmed_teams(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/team/{G.team1_name}/invite_member/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_detail.html"]))


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_invitation_post_creates_invitation(client_with_logged_user1):
    user2_id = User.objects.get(username=G.user2_name).id
    response = client_with_logged_user1.post(f"/team/{G.team1_name}/invite_member/",
                                             {"user": user2_id,
                                              "add_member": "Submit+Query"},
                                             follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "team_detail.html"]))
    soup = BeautifulSoup(response.content)
    assert Invitation.objects.filter(user_id=user2_id, team_id=G.team1_name).exists()
    assert soup.select(".messages li")[
               0].text == f"User {G.user2_name} was invited. User's can confirm or deny invitation."
