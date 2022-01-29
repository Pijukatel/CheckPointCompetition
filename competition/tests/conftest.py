import os

import pytest
from django.core.management import call_command
from django.test import Client
from selenium import webdriver

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
def load_point1_no_photo():
    call_command('loaddata', 'test_point_1_no_photo.json')


@pytest.mark.django_db
@pytest.fixture
def load_point1_confirmed():
    call_command('loaddata', 'test_point_1_confirmed.json')


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


@pytest.fixture(autouse=True, scope="session")
def delete_test_images():
    yield None
    for root, dirs, files in os.walk(f"static/images/", topdown=False):
        for name in files:
            if name.startswith("test_image") and name.endswith(".jpg"):
                os.remove(os.path.join(root, name))


@pytest.fixture()
def delete_test_image():
    """Fixture to remove test image before the test that is going to create it."""
    for folder in ("images", "points", "teams"):
        try:
            os.remove(f'static/images/{folder}/{G.test_image_name}')
        except FileNotFoundError:
            pass

@pytest.fixture(scope='session')
def browser_factory():
    class ContextBrowser:
        def __init__(self):
            path_to_gecko_driver_exe = os.path.join(os.path.dirname(__file__), G.path_to_gecko_driver)
            self.driver = webdriver.Firefox(executable_path=path_to_gecko_driver_exe)

        def __enter__(self):
            return self.driver

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.driver.quit()

    return ContextBrowser
