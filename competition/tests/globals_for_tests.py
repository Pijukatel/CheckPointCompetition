"""This file contains globals used in tests.
Motivation:
    1 - Less repetition.
    2 - Single point of entry.
    3 - Possibility to easy use as parameters in parametrized tests(unlike fixtures!)"""
from typing import NamedTuple


class Globals(NamedTuple):
    APP_NAME = 'competition'
    user1_name = 'TestName1'
    user1_password = 'TestPassword1234'
    user2_name = 'TestName2'
    user2_password = user1_password
    checkpoint1_name = 'TestCheckPoint1'
    checkpoint1_description = 'TestDescription'
    checkpoint1_lon = '21.6543'
    checkpoint1_lat = '12.3456'
    checkpoint2_name = 'TestCheckPoint2'


G = Globals
