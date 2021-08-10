from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pytest_django.asserts import assertTemplateUsed

from .globals_for_tests import G
from ..models import Team, Membership, delete_empty_teams


def create_team(client, name=G.team1_name):
    response = client.post('/team/create/',
                           {'name': name},
                           follow=True)
    return response


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_user_detail_show_team_membership(client_with_logged_user1):
    response = client_with_logged_user1.get('/accounts/user/', follow=True)
    assert response.status_code == 200
    assert bytes(G.team1_name, encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_user_detail_contains_leave_team_link(client_with_logged_user1):
    response = client_with_logged_user1.get('/accounts/user/', follow=True)
    assert bytes('href="/team/leave/"', encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_team_detail_show_team_members(client):
    response = client.get(f'/team/{G.team1_name}/', follow=True)
    assert response.status_code == 200
    assert bytes(f'{G.user1_name}', encoding=response.charset) in response.content
    assert bytes(f'{G.user2_name}', encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_team_detail_show_leave_link_only_to_logged_user(client_with_logged_user1):
    response = client_with_logged_user1.get(f'/team/{G.team1_name}/', follow=True)
    assert bytes(f'{G.user1_name}\n                \n                     <a href="/team/leave/"',
                 encoding=response.charset) in response.content
    assert bytes(f'{G.user2_name}\n                \n                     <a href="/team/leave/"',
                 encoding=response.charset) not in response.content


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


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_leave_team(client_with_logged_user1):
    client_with_logged_user1.get(f'/team/leave/', follow=True)
    with pytest.raises(ObjectDoesNotExist):
        Membership.objects.get(team__name=G.team1_name, user__username=G.user1_name)


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_leave_team_redirect(client_with_logged_user1):
    response = client_with_logged_user1.get(f'/team/leave/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'user_detail.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_auto_delete_empty_team(client_with_logged_user1):
    client_with_logged_user1.get(f'/team/leave/', follow=True)
    with pytest.raises(ObjectDoesNotExist):
        Team.objects.get(name=G.team1_name)


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.usefixtures('load_registered_user2')
@pytest.mark.django_db
def test_add_member_to_team(client_with_logged_user1):
    client_with_logged_user1.post(f'/team/{G.team1_name}/add_member/',
                                  {'user': User.objects.get(username=G.user2_name).id},
                                  follow=True)
    assert Membership.objects.filter(user__username=G.user2_name, team__name=G.team1_name).exists()


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.usefixtures('load_registered_user2')
@pytest.mark.django_db
def test_add_member_to_team_redirect(client_with_logged_user1):
    response = client_with_logged_user1.post(f'/team/{G.team1_name}/add_member/',
                                             {'user': User.objects.get(username=G.user2_name).id},
                                             follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_detail.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_update(client_with_logged_user1):
    response = client_with_logged_user1.get(f'/team/{G.team1_name}/update/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_update.html']))


@pytest.mark.usefixtures('load_registered_user1_with_confirmed_team1')
@pytest.mark.django_db
def test_confirmed_team_update_redirect(client_with_logged_user1):
    response = client_with_logged_user1.get(f'/team/{G.team1_name}/update/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_detail.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_update_unauthenticated_redirect(client):
    response = client.get(f'/team/{G.team1_name}/update/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'login.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.usefixtures('load_registered_user2')
@pytest.mark.django_db
def test_team_update_unauthorized(client_with_logged_user2):
    """Only team members can edit team."""
    response = client_with_logged_user2.get(f'/team/{G.team1_name}/update/', follow=True)
    assert response.status_code == 403


@pytest.mark.usefixtures('delete_test_team_image')
@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_update_photo_redirect(client_with_logged_user1):
    with open('competition/fixtures/test_image.jpg', 'rb') as fp:
        response = client_with_logged_user1.post(f'/team/{G.team1_name}/update/', {'photo': fp}, follow=True)
        assert response.status_code == 200
        assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_detail.html']))


@pytest.mark.usefixtures('delete_test_team_image')
@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_update_photo_team_updated(client_with_logged_user1):
    with open('competition/fixtures/test_image.jpg', 'rb') as fp:
        response = client_with_logged_user1.post(f'/team/{G.team1_name}/update/', {'photo': fp}, follow=True)
        assert bytes(f'<img src="/images/teams/{G.test_image_name}', response.charset) in response.content


@pytest.mark.usefixtures('load_team2')
@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_auto_delete_empty_team():
    delete_empty_teams()
    teams = Team.objects.all()
    assert len(teams) == 1
    assert teams[0].name == G.team1_name


@pytest.mark.usefixtures('load_team2')
@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_auto_delete_empty_team_called_on_membership_save():
    with patch('competition.models.delete_empty_teams', return_value=None) as mocked:
        Membership.objects.all()[0].save()
    assert mocked.called


@pytest.mark.django_db
def test_team_list_view_template(client):
    response = client.get('/teams/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_list.html']))


@pytest.mark.usefixtures('load_team2')
@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_list_view_template_contains_teams(client):
    response = client.get('/teams/', follow=True)
    assert bytes(f'{G.team1_name}', response.charset) in response.content
    assert bytes(f'{G.team2_name}', response.charset) in response.content


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_team_delete_template(client_with_logged_user1):
    response = client_with_logged_user1.get(f'/team/{G.team1_name}/delete/', follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'team_delete.html']))


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.usefixtures('load_registered_user2')
@pytest.mark.django_db
def test_team_delete_unauthorized(client_with_logged_user2):
    response = client_with_logged_user2.get(f'/team/{G.team1_name}/delete/', follow=True)
    assert response.status_code == 403


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_delete_team1_deleted_from_db(client_with_logged_user1):
    client_with_logged_user1.post(f'/team/{G.team1_name}/delete/',
                                  {},
                                  follow=True)
    with pytest.raises(ObjectDoesNotExist):
        Team.objects.get(name=G.team1_name)