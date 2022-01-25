# Not a unit test. Full system test.
"""
Following procedure is tested which simulates expected use.

Competition countdown
Competition pre-start (open for registration)

4 user creation
2 teams creation
each team confirmation


competition start
4 user creation
2 teams creation
confirm on team
deny other team
team1 visit checkpoint1 8:00
team2 visit checkpoint1 8:01
team3 visit checkpoint2 8:02
confirm all three visits
team3 visit checkpoint1
deny last visit ("bad photo...")
leaderboard 1,2,3
team2 visits checkopoit2
confirm visit
leaderboard 2,1,3
Stop competition
team3 visits checkpoint (but upload photo is disabled) -> competition end
"""

import pytest
from .globals_for_tests import G
from ..models import Team, Membership
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User


# Competition countdown
# Competition pre-start (open for registration)
# 4 user creation
# 2 teams creation
# Upload team photos
# Admin login
# each team confirmation

class TestSetup:
    wait = 1
    teams = {
        "TestTeam1": ("TestUser1", "TestUser2"),
        "TestTeam2": ("TestUser3", "TestUser4"),
    }
    password = "TestPassword123"


def create_user(username, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Create Account")))
    browser.find_element_by_link_text("Create Account").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_username")))
    browser.find_element_by_id("id_username").send_keys(username)
    browser.find_element_by_id("id_password1").send_keys(TestSetup.password)
    browser.find_element_by_id("id_password2").send_keys(TestSetup.password)
    browser.find_element_by_id("create_user_button").click()
    assert User.objects.filter(username=username).exists()


def login(username, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Login")))
    browser.find_element_by_link_text("Login").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_username")))
    browser.find_element_by_id("id_username").send_keys(username)
    browser.find_element_by_id("id_password").send_keys(TestSetup.password)
    browser.find_element_by_id("log_in_button").click()
    browser.username = username


def logged_user_creates_team(team_name, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Create new team")))
    browser.find_element_by_link_text("Create new team").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_name")))
    browser.find_element_by_id("id_name").send_keys(team_name)
    browser.find_element_by_id("create_team_button").click()
    assert Team.objects.filter(name=team_name).exists()
    assert Membership.objects.filter(user__username=browser.username, team__name=team_name).exists()


def add_user_to_team(team_name, username, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, team_name)))
    browser.find_element_by_link_text(team_name).click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Add member.")))
    browser.find_element_by_link_text("Add member.").click()

    select = Select(browser.find_element_by_id('id_user'))
    select.select_by_visible_text(username)
    browser.find_element_by_id("add_member_button").click()
    assert Membership.objects.filter(user__username=browser.username, team__name=team_name).exists()
    assert Membership.objects.filter(user__username=username, team__name=team_name).exists()


@pytest.mark.functional
def test_system(live_server, browser_factory):
    # Register first user
    with browser_factory() as browser:
        browser.get(G.test_address)
        create_user(TestSetup.teams["TestTeam1"][0], browser)
        login(TestSetup.teams["TestTeam1"][0], browser)
        logged_user_creates_team("TestTeam1", browser)

    # Register second user
    with browser_factory() as browser:
        browser.get(G.test_address)
        create_user(TestSetup.teams["TestTeam1"][1], browser)
        login(TestSetup.teams["TestTeam1"][1], browser)

    # Register third and fourth user.
    for username in TestSetup.teams["TestTeam2"]:
        with browser_factory() as browser:
            browser.get(G.test_address)
            create_user(username, browser)
            login(username, browser)

    # User 1 adds user 2 to the team
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(TestSetup.teams["TestTeam1"][0], browser)
        add_user_to_team("TestTeam1", TestSetup.teams["TestTeam1"][1], browser)

    # Third user creates team and adds fourth user
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(TestSetup.teams["TestTeam2"][0], browser)
        logged_user_creates_team("TestTeam2", browser)
        add_user_to_team("TestTeam2", TestSetup.teams["TestTeam2"][1], browser)

    # Both teams upload photos

    # Both photos are confirmed
