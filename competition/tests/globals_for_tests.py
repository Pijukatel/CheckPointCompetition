"""This file contains globals used in tests.
Motivation:
    1 - Less repetition.
    2 - Single point of entry.
    3 - Possibility to easy use as parameters in parametrized tests(unlike fixtures!)"""
from typing import NamedTuple


class Globals(NamedTuple):
    APP_NAME = "competition"
    user1_name = "TestName1"
    user1_password = "TestPassword1234"
    user2_name = "TestName2"
    user2_password = user1_password
    user_staff_name = "TestNameStaff"
    user_staff_password = user1_password
    checkpoint1_name = "TestCheckPoint1"
    checkpoint1_description = "TestDescription"
    checkpoint1_lon = "12.013"
    checkpoint1_lat = "57.797"
    checkpoint2_name = "TestCheckPoint2"
    checkpoint2_lon = "12.012"
    checkpoint2_lat = "57.686"
    team1_name = "TestTeam1"
    team2_name = "TestTeam2"
    test_image_name = "test_image.jpg"
    test_point_photo_name = "SomePhoto.jpg"
    test_address='http://127.0.0.1:8000/'
    path_to_gecko_driver = r'geckodriver\geckodriver.exe'


G = Globals
