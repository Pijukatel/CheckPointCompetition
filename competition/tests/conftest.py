import pytest
import os

from django.test import Client
from django.core.management import call_command

from competition.tests.globals_for_tests import G

'''
# This is global fixture that is called by just being defined here???
@pytest.fixture(scope='function')  # https://docs.pytest.org/en/latest/how-to/fixtures.html#fixture-scopes
def django_db_setup(django_db_setup, django_db_blocker):
    # 'Unused' parameter django_db_setup is internal fixture for creating test database
    # https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-don-t-use-transactional-or-live-server
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_user_1.json')
'''


@pytest.mark.django_db
@pytest.fixture
def load_registered_user1():
    call_command('loaddata', 'test_user_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user1_with_team1():
    call_command('loaddata', 'test_user_1_with_team_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user1_with_confirmed_team1():
    call_command('loaddata', 'test_user_1_with_confirmed_team_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_users_1_2_with_team1():
    call_command('loaddata', 'test_users_1_2_with_team_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_team2():
    call_command('loaddata', 'test_team_2.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user2_with_team2():
    call_command('loaddata', 'test_user_2_with_team_2.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user2_with_team2_no_photo():
    call_command('loaddata', 'test_user_2_with_team_2_no_photo.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user2():
    call_command('loaddata', 'test_user_2.json')


@pytest.mark.django_db
@pytest.fixture
def load_registered_user_with_is_staff():
    call_command('loaddata', 'test_user_with_is_staff.json')


@pytest.mark.django_db
@pytest.fixture
def load_checkpoint1():
    call_command('loaddata', 'test_checkpoint_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_checkpoint2():
    call_command('loaddata', 'test_checkpoint_2.json')


@pytest.mark.django_db
@pytest.fixture
def load_point1():
    call_command('loaddata', 'test_point_1.json')


@pytest.mark.django_db
@pytest.fixture
def load_point2():
    call_command('loaddata', 'test_point_2.json')


@pytest.mark.django_db
@pytest.fixture
def load_point3_of_team2():
    call_command('loaddata', 'test_point_3_of_team2.json')


@pytest.fixture
def client_with_logged_user1():
    """Return client with logged in user1."""
    client = Client()
    client.login(username=G.user1_name, password=G.user1_password)
    return client


@pytest.fixture
def client_with_logged_user2():
    """Return client with logged in user2."""
    client = Client()
    client.login(username=G.user2_name, password=G.user2_password)
    return client


@pytest.fixture
def client_with_logged_user_staff(load_registered_user_with_is_staff):
    """Return client with logged in user with is_staff=True."""
    client = Client()
    client.login(username=G.user_staff_name, password=G.user_staff_password)
    return client


@pytest.fixture()
def delete_test_team_image():
    """Cleanup fixture to remove test image after uploading it in test."""
    yield None
    os.remove(f'static/images/teams/{G.test_image_name}')


@pytest.fixture()
def delete_test_point_image():
    """Cleanup fixture to remove test image after uploading it in test."""
    yield None
    os.remove(f'static/images/points/{G.test_image_name}')