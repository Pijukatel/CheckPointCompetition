import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ..models import Team, Membership


def create_team(client, name=G.team1_name):
    response = client.post('/team/create/',
                           {'name': name},
                           follow=True)
    return response

@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_user_detail_show_team_membership(client_with_logged_user1):
    response = client_with_logged_user1.get('/accounts/user/', Follow=True)
    assert response.status_code == 200
    assert bytes(G.team1_name, encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_team_detail_show_team_members(client):
    response = client.get(f'/team/{G.team1_name}/', Follow=True)
    assert response.status_code == 200
    assert bytes(f'<li>{G.user1_name}</li>', encoding=response.charset) in response.content
    assert bytes(f'<li>{G.user2_name}</li>', encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_user1')
@pytest.mark.django_db
def test_create_team(client_with_logged_user1):
    response = create_team(client_with_logged_user1)
    assert response.status_code == 200
    team = Team.objects.filter(name=G.team1_name)
    assert team.exists()


@pytest.mark.usefixtures('load_registered_user1')
@pytest.mark.django_db
def test_create_team_redirect(client_with_logged_user1):
    response = create_team(client_with_logged_user1)
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_detail.html']))


@pytest.mark.usefixtures('load_registered_user1')
@pytest.mark.django_db
def test_team_creator_becomes_member(client_with_logged_user1):
    create_team(client_with_logged_user1)
    assert Membership.objects.filter(user__username=G.user1_name, team__name=G.team1_name).exists()


def test_leave_team():
    assert False


def test_auto_delete_empty_team():
    assert False
