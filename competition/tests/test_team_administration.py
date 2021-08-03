import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_user_detail_show_team_membership(client_with_logged_user1):
    response = client_with_logged_user1.get('/accounts/user/', Follow=True)
    assert response.status_code == 200
    assert bytes(f'Team: {G.team1_name}', encoding=response.charset) in response.content


@pytest.mark.usefixtures('load_registered_users_1_2_with_team1')
@pytest.mark.django_db
def test_team_detail_show_team_members(client):
    response = client.get(f'/team/{G.team1_name}/', Follow=True)
    assert response.status_code == 200
    assert bytes(f'<li>{G.user1_name}</li>', encoding=response.charset) in response.content
    assert bytes(f'<li>{G.user2_name}</li>', encoding=response.charset) in response.content