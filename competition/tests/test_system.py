# Not a unit test. Full system test.
"""
Following procedure is tested which simulates expected use.

    With two created checkpoints.
Competition countdown
Register not possible.

Competition pre-start (open for registration)
    4 user creation
    2 teams creation
    Upload team photos
    Admin login
    each team confirmation
Checkpoint view not possible

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
from contextlib import ExitStack

import pytest
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from freezegun import freeze_time
from datetime import timedelta

from .globals_for_tests import G
from ..models import Team, Membership, Point, Invitation
from competition.settings import COUNTDOWN, PRE_REGISTRATION, COMPETITION, ARCHIVED


class TestSetup:
    wait = 1
    teams = {
        "TestTeam1": ("TestUser1", "TestUser2"),
        "TestTeam2": ("TestUser3", "TestUser4"),
        "TestTeam3": ("TestUser5", "TestUser6"),
        "TestTeam4": ("TestUser7", "TestUser8"),
    }
    password = G.user1_password
    image_name = "test_image.jpg"
    image = Image.frombytes("L", (3, 2), b'\xbf\x8cd\xba\x7f\xe0\xf0\xb8t\xfe')


def create_user_closed(browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Create Account")))
    browser.find_element_by_link_text("Create Account").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.CLASS_NAME, "Message_info")))
    assert (browser.find_element_by_class_name("Message_info").text
            == f"Competition will be open for registration: {PRE_REGISTRATION.isoformat()}")
    browser.find_element_by_id("home")


def checkpoints_closed(browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Checkpoints")))
    browser.find_element_by_link_text("Checkpoints").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.CLASS_NAME, "Message_info")))
    assert (browser.find_element_by_class_name("Message_info").text
            == f"Competition will start: {COMPETITION.isoformat()}")
    browser.find_element_by_id("home")


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


def send_invite(browser, invited_user):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "team_link")))
    team_link = browser.find_element_by_id("team_link")
    team_name = team_link.text
    team_link.click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Invite member.")))
    browser.find_element_by_link_text("Invite member.").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_user")))
    select = Select(browser.find_element_by_id("id_user"))
    select.select_by_visible_text(invited_user)
    browser.find_element_by_id("invite_member_button").click()
    assert Invitation.objects.filter(user__username=invited_user, team__name=team_name).exists()

def accept_invite(browser, team_to_accept):
    browser.get(G.test_address)
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.CLASS_NAME, "Message_invitations")))
    browser.find_element_by_xpath(f'//a[contains(@href,"/team/{team_to_accept}/accept/")]').click()
    user = browser.find_element_by_id("logged_user_link").text
    assert Membership.objects.filter(user__username=user, team_id=team_to_accept)

def logged_user_in_team_upload_team_photo(team_name, image_path, browser):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, team_name)))
    browser.find_element_by_link_text(team_name).click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Upload photo.")))
    browser.find_element_by_link_text("Upload photo.").click()
    browser.find_element_by_id("id_photo").send_keys(str(image_path))
    browser.find_element_by_id("upload_photo_button").click()
    assert Team.objects.filter(name=team_name)[0].photo.name.startswith(f"teams/{TestSetup.image_name[:-4]}")


def staff_user_confirm_team_photo(browser, deny=False):
    browser.get(G.test_address + "team/photo-confirm/")
    if deny:
        deny_reason = "some reason"
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_deny_reason")))
        browser.find_element_by_id("id_deny_reason").send_keys(deny_reason)
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "deny_button")))
        team_name = browser.find_element_by_id("TeamName").text
        browser.find_element_by_id("deny_button").click()
        assert not Team.objects.get(name=team_name).confirmed
        assert Team.objects.get(name=team_name).deny_reason == deny_reason
    else:
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


def staff_user_confirm_point_photo(browser, deny=False):
    browser.get(G.test_address + "point/photo-confirm/")
    if deny:
        deny_reason = "some reason"
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "id_deny_reason")))
        browser.find_element_by_id("id_deny_reason").send_keys(deny_reason)
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "deny_button")))
        browser.find_element_by_id("deny_button").click()
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "TeamName")))
        team_name = browser.find_element_by_id("TeamName").text
        checkpoint_name = browser.find_element_by_id("CheckpointName").text
        point = Point.objects.get(checkpoint_id=checkpoint_name, team_id=team_name)
        assert not point.confirmed
        assert point.deny_reason == deny_reason
    else:
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "confirm_button")))
        browser.find_element_by_id("confirm_button").click()
        WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "TeamName")))
        team_name = browser.find_element_by_id("TeamName").text
        checkpoint_name = browser.find_element_by_id("CheckpointName").text
        point = Point.objects.get(checkpoint_id=checkpoint_name, team_id=team_name)
        assert point.confirmed
        assert not point.deny_reason


def check_expected_positions(browser, positions):
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.LINK_TEXT, "Teams")))
    browser.find_element_by_link_text("Teams").click()
    WebDriverWait(browser, TestSetup.wait).until(EC.presence_of_element_located((By.ID, "scoreBoard")))
    rows = browser.find_element_by_id("scoreBoard").find_elements_by_tag_name("tr")
    for row, expected_team in zip(rows, positions):
        assert row.find_elements_by_tag_name("a")[0].text == expected_team


@pytest.mark.disable_default_time
@pytest.mark.functional
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
def test_system(live_server, browser_factory, tmp_path, load_registered_user_with_is_staff):
    # Prepare universal image for download
    image_path = tmp_path / TestSetup.image_name
    TestSetup.image.save(image_path)

    with ExitStack() as stack:

        with freeze_time(COUNTDOWN + timedelta(seconds=1)):
            # Registration is closed.
            anonymous_browser = stack.enter_context(browser_factory())
            anonymous_browser.get(G.test_address)
            create_user_closed(anonymous_browser)

        with freeze_time(PRE_REGISTRATION + timedelta(seconds=1)):
            # Checkpoints are closed.
            anonymous_browser.get(G.test_address)
            checkpoints_closed(anonymous_browser)

            # Register first user
            user1_browser = stack.enter_context(browser_factory())
            user1_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam1"][0], user1_browser)
            login(TestSetup.teams["TestTeam1"][0], user1_browser)
            logged_user_creates_team("TestTeam1", user1_browser)

            # Register second user
            user2_browser = stack.enter_context(browser_factory())
            user2_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam1"][1], user2_browser)
            login(TestSetup.teams["TestTeam1"][1], user2_browser)

            # Register third user
            user3_browser = stack.enter_context(browser_factory())
            user3_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam2"][0], user3_browser)
            login(TestSetup.teams["TestTeam2"][0], user3_browser)

            # Register fourth user
            user4_browser = stack.enter_context(browser_factory())
            user4_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam2"][1], user4_browser)
            login(TestSetup.teams["TestTeam2"][1], user4_browser)

            # User 1 adds user 2 to the team
            user1_browser.get(G.test_address)
            send_invite(user1_browser, TestSetup.teams["TestTeam1"][1])
            accept_invite(user2_browser, "TestTeam1")

            # Third user creates team and adds fourth user, upload team photo
            user3_browser.get(G.test_address)
            logged_user_creates_team("TestTeam2", user3_browser)
            send_invite(user3_browser, TestSetup.teams["TestTeam2"][1])
            accept_invite(user4_browser, "TestTeam2")
            logged_user_in_team_upload_team_photo("TestTeam2", image_path, user3_browser)

            # User1 uploads team1 photo
            user1_browser.get(G.test_address)
            logged_user_in_team_upload_team_photo("TestTeam1", image_path, user1_browser)

            # Both photos are confirmed by staff user
            staff_browser = stack.enter_context(browser_factory())
            staff_browser.get(G.test_address)
            login(G.user_staff_name, staff_browser)
            staff_user_confirm_team_photo(staff_browser)
            staff_user_confirm_team_photo(staff_browser)

        with freeze_time(COMPETITION + timedelta(seconds=1)):
            # Start competition
            # Team 2 visit checkpoint 1
            user4_browser.get(G.test_address)
            logged_user_in_team_upload_point_photo(user4_browser, "TestTeam2", G.checkpoint1_name, image_path)

        with freeze_time(COMPETITION + timedelta(seconds=2)):
            # Team 1 visit checkpoint 1
            user2_browser.get(G.test_address)
            logged_user_in_team_upload_point_photo(user2_browser, "TestTeam1", G.checkpoint1_name, image_path)

            # Admin confirms visits
            staff_user_confirm_point_photo(staff_browser)
            staff_user_confirm_point_photo(staff_browser)

            # Leader board 2,1 (same points, but team1 later point upload)
            anonymous_browser.get(G.test_address)
            check_expected_positions(anonymous_browser, positions=("TestTeam2", "TestTeam1"))

            # Register fifth and sixth user.
            # Register fifth user
            user5_browser = stack.enter_context(browser_factory())
            user5_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam3"][0], user5_browser)
            login(TestSetup.teams["TestTeam3"][0], user5_browser)

            # Register sixth user
            user6_browser = stack.enter_context(browser_factory())
            user6_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam3"][1], user6_browser)
            login(TestSetup.teams["TestTeam3"][1], user6_browser)

            # Fifth user creates team and adds sixth user, upload team photo
            logged_user_creates_team("TestTeam3", user5_browser)
            send_invite(user5_browser, TestSetup.teams["TestTeam3"][1])
            accept_invite(user6_browser, "TestTeam3")
            logged_user_in_team_upload_team_photo("TestTeam3", image_path, user5_browser)

            # Team3 photo is confirmed by staff user
            staff_user_confirm_team_photo(staff_browser)

            # Leader board 2,1,3
            anonymous_browser.get(G.test_address)
            check_expected_positions(anonymous_browser, positions=("TestTeam2", "TestTeam1", "TestTeam3"))

            # Register seventh and eight user.
            # Register seventh user
            user7_browser = stack.enter_context(browser_factory())
            user7_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam4"][0], user7_browser)
            login(TestSetup.teams["TestTeam4"][0], user7_browser)

            # Register seventh user
            user8_browser = stack.enter_context(browser_factory())
            user8_browser.get(G.test_address)
            create_user(TestSetup.teams["TestTeam4"][1], user8_browser)
            login(TestSetup.teams["TestTeam4"][1], user8_browser)

            # Seventh user creates team and adds Eighth user, upload team photo
            user7_browser.get(G.test_address)
            logged_user_creates_team("TestTeam4", user7_browser)
            send_invite(user7_browser, TestSetup.teams["TestTeam4"][1])
            accept_invite(user8_browser, "TestTeam4")
            logged_user_in_team_upload_team_photo("TestTeam4", image_path, user7_browser)

            # Team4 photo is denied by staff user
            staff_browser.get(G.test_address)
            staff_user_confirm_team_photo(staff_browser, deny=True)

        with freeze_time(COMPETITION + timedelta(seconds=3)):
            # team3 visits checkpoint2, checkpoint1 in t + 3
            user6_browser.get(G.test_address)
            team = "TestTeam3"
            logged_user_in_team_upload_point_photo(user6_browser, team, G.checkpoint1_name, image_path)
            logged_user_in_team_upload_point_photo(user6_browser, team, G.checkpoint2_name, image_path)

            # Admin confirms visits
            staff_user_confirm_point_photo(staff_browser)
            staff_user_confirm_point_photo(staff_browser)

            # Leader board 3,2,1,4
            anonymous_browser.get(G.test_address)
            check_expected_positions(anonymous_browser, positions=("TestTeam3", "TestTeam2", "TestTeam1", "TestTeam4"))

            # Team 2 visit checkpoint 2
            logged_user_in_team_upload_point_photo(user3_browser, "TestTeam2", G.checkpoint2_name, image_path)

            # Admin deny visit
            staff_user_confirm_point_photo(staff_browser, deny=True)

            # Leader board 3,2,1,4
            anonymous_browser.get(G.test_address)
            check_expected_positions(anonymous_browser, positions=("TestTeam3", "TestTeam2", "TestTeam1", "TestTeam4"))

        with freeze_time(COMPETITION + timedelta(seconds=4)):
            # team1 visits checkpoint2 in t + 4
            logged_user_in_team_upload_point_photo(user1_browser, "TestTeam1", G.checkpoint2_name, image_path)

            # Admin confirms visit
            staff_user_confirm_point_photo(staff_browser)

            # Leader board 3,1,2,4
            check_expected_positions(anonymous_browser, positions=("TestTeam3", "TestTeam1", "TestTeam2", "TestTeam4"))
