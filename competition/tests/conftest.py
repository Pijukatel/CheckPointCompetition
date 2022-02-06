import os

import pytest
from unittest import mock
from django.test import Client
from selenium import webdriver
from datetime import datetime, timedelta
from competition.middleware.time_middleware import Stage, redirect_to_countdown, return_normal_response
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


@pytest.fixture(scope="session", autouse=True)
def far_future():
    return datetime.now() + timedelta(seconds=1000)


@pytest.fixture(autouse=True)
def in_competition(request, far_future):
    if 'disable_default_time' in request.keywords:
        yield
    else:
        now = datetime.now()
        stages_start_times = (
            Stage(now - timedelta(seconds=3), "countdown", redirect_to_countdown),
            Stage(now - timedelta(seconds=2), "pre_registration", return_normal_response),
            Stage(now - timedelta(seconds=1), "competition", return_normal_response),
            Stage(far_future, "archived", return_normal_response),
        )
        with (
                mock.patch("competition.middleware.time_middleware.get_current_stage.__defaults__",
                           (stages_start_times,)),
                mock.patch("competition.middleware.time_middleware.COUNTDOWN", (now - timedelta(seconds=3))),
                mock.patch("competition.middleware.time_middleware.PRE_REGISTRATION", (now - timedelta(seconds=2))),
                mock.patch("competition.middleware.time_middleware.COMPETITION", (now - timedelta(seconds=1))),
                mock.patch("competition.middleware.time_middleware.ARCHIVED", far_future),
        ):
            yield


@pytest.fixture
def in_countdown(far_future):
    stages_start_times = (
        Stage(datetime.now() - timedelta(seconds=3), "countdown", redirect_to_countdown),
        Stage(far_future, "pre_registration", return_normal_response),
        Stage(far_future, "competition", return_normal_response),
        Stage(far_future, "archived", return_normal_response),
    )
    with (mock.patch("competition.middleware.time_middleware.get_current_stage.__defaults__", (stages_start_times,)),
          mock.patch("competition.middleware.time_middleware.PRE_REGISTRATION", far_future)):
        yield


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
