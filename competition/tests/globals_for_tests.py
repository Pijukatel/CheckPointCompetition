"""This file contains globals used in tests.
Motivation:
    1 - Less repetition.
    2 - Single point of entry.
    3 - Possibility to easy use as parameters in parametrized tests(unlike fixtures!)"""
from typing import NamedTuple
from datetime import datetime, timedelta
import pytz


class Globals(NamedTuple):
    APP_NAME = "competition"
    user1_name = "TestName1"
    user1_password = "TestPassword1234"
    user1_lats = [57.68694, 6.0]
    user1_lons = [12.0129, 7.0]
    user2_name = "TestName2"
    user2_password = user1_password
    user2_lats = [0]
    user2_lons = [0]
    user3_name = "TestName3"
    user3_password = user1_password
    user4_name = "TestName4"
    user4_password = user1_password
    user_staff_name = "TestNameStaff"
    user_staff_password = user1_password
    checkpoint1_name = "TestCheckPoint1"
    checkpoint1_description = "TestDescription"
    checkpoint2_description = checkpoint1_description
    checkpoint3_description = checkpoint1_description
    checkpoint1_lon = 12.013
    checkpoint1_lat = 57.797
    checkpoint2_name = "TestCheckPoint2"
    checkpoint2_lon = 12.012
    checkpoint2_lat = 57.686
    checkpoint3_name = "TestCheckPoint3"
    checkpoint3_lon = 12.014
    checkpoint3_lat = 57.801
    checkpoint1_image_name = "test_image_checkpoint1.jpg"
    checkpoint2_image_name = "test_image_checkpoint2.jpg"
    checkpoint3_image_name = "test_image_checkpoint3.jpg"
    point1_image_name = "test_image_point1.jpg"
    point1_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=2, minute=10))
    point2_image_name = "test_image_point2.jpg"
    point2_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=2, minute=20))
    point3_image_name = "test_image_point3.jpg"
    point3_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=2, minute=30))
    team1_name = "TestTeam1"
    team1_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=1, minute=10))
    team2_name = "TestTeam2"
    team2_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=1, minute=20))
    team3_name = "TestTeam3"
    team3_photo_confirmation_date = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=1, minute=20))
    test_image_name = "test_image.jpg"
    test_point_photo_name = "SomePhoto.jpg"
    test_address = 'http://127.0.0.1:8000/'
    path_to_gecko_driver = r'geckodriver\geckodriver.exe'


G = Globals
