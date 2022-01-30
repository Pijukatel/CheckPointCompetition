# Not a unit test. Full system test.
"""
Following procedure is tested which simulates expected use.

Current state:

4 user creation
2 teams creation
Upload team photos
Admin login
each team confirmation

Desired state:

Competition countdown
Competition pre-start (open for registration)

4 user creation
2 teams creation
Upload team photos
Admin login
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
from PIL import Image

from .globals_for_tests import G
from ..models import Team, Membership, Point
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User


class TestSetup:
    wait = 1
    teams = {
        "TestTeam1": ("TestUser1", "TestUser2"),
        "TestTeam2": ("TestUser3", "TestUser4"),
    }
    password = G.user1_password
    image_name = "test_image.jpg"
    image = Image.frombytes("L", (3, 2), b'\xbf\x8cd\xba\x7f\xe0\xf0\xb8t\xfe')


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


def logged_user_in_team_upload_team_photo(team_name, image_path, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, team_name)))
    browser.find_element_by_link_text(team_name).click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Upload photo.")))
    browser.find_element_by_link_text("Upload photo.").click()
    browser.find_element_by_id("id_photo").send_keys(str(image_path))
    browser.find_element_by_id("upload_photo_button").click()
    assert Team.objects.filter(name=team_name)[0].photo.name.startswith(f"teams/{TestSetup.image_name[:-4]}")


def staff_user_confirm_team_photo(browser):
    browser.get(G.test_address + "team/photo-confirm/")
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "confirm_button")))
    team_name = browser.find_element_by_id("TeamName").text
    browser.find_element_by_id("confirm_button").click()
    assert Team.objects.get(name=team_name).confirmed


def logged_user_in_team_upload_point_photo(browser, team_name, checkpoint_name, image_path):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Checkpoints")))
    browser.find_element_by_link_text("Checkpoints").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, checkpoint_name)))
    browser.find_element_by_link_text(checkpoint_name).click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_photo")))
    browser.find_element_by_id("id_photo").send_keys(str(image_path))
    browser.find_element_by_id("upload_photo_button").click()

    point_querry = Point.objects.filter(team_id=team_name, checkpoint_id=checkpoint_name)
    assert point_querry.exists()
    point = point_querry.get()
    assert not point.confirmed
    assert point.photo.name.startswith(f"points/{TestSetup.image_name[:-4]}")
    assert not point.deny_reason


def staff_user_confirm_point_photo(browser):
    browser.get(G.test_address + "point/photo-confirm/")
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "confirm_button")))
    browser.find_element_by_id("confirm_button").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "TeamName")))
    team_name = browser.find_element_by_id("TeamName").text
    checkpoint_name = browser.find_element_by_id("CheckpointName").text
    point = Point.objects.get(checkpoint_id=checkpoint_name, team_id=team_name)
    assert point.confirmed
    assert not point.deny_reason


@pytest.mark.functional
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
def test_system(live_server, browser_factory, tmp_path, load_registered_user_with_is_staff):
    # Prepare universal image for download
    image_path = tmp_path / TestSetup.image_name
    TestSetup.image.save(image_path)

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

    # Third user creates team and adds fourth user, upload team photo
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(TestSetup.teams["TestTeam2"][0], browser)
        logged_user_creates_team("TestTeam2", browser)
        add_user_to_team("TestTeam2", TestSetup.teams["TestTeam2"][1], browser)
        logged_user_in_team_upload_team_photo("TestTeam2", image_path, browser)

    # User1 uploads team1 photo
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(TestSetup.teams["TestTeam1"][0], browser)
        logged_user_in_team_upload_team_photo("TestTeam1", image_path, browser)

    # Both photos are confirmed by staff user
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(G.user_staff_name, browser)
        staff_user_confirm_team_photo(browser)
        staff_user_confirm_team_photo(browser)

    # Start competition
    # Register another other team

    # TODO: Add time keeping test for leaderboard (check photo upload datetime)
    # Team 1,2 visit checkpoint 1
    with browser_factory() as browser:
        browser.get(G.test_address)
        team = "TestTeam1"
        login(TestSetup.teams[team][1], browser)
        logged_user_in_team_upload_point_photo(browser, team, G.checkpoint1_name, image_path)

    with browser_factory() as browser:
        browser.get(G.test_address)
        team = "TestTeam2"
        login(TestSetup.teams[team][1], browser)
        logged_user_in_team_upload_point_photo(browser, team, G.checkpoint1_name, image_path)

    # Admin confirms visits
    with browser_factory() as browser:
        browser.get(G.test_address)
        login(G.user_staff_name, browser)
        staff_user_confirm_point_photo(browser)
        staff_user_confirm_point_photo(browser)
    # Leader board
