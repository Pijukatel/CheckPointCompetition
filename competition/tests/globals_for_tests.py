"""This file contains globals used in tests.
Motivation:
    1 - Less repetition.
    2 - Single point of entry.
    3 - Possibility to easy use as parameters in parametrized tests(unlike fixtures!)"""
from typing import NamedTuple


class Globals(NamedTuple):
    APP_NAME = 'competition'
    user1_name = 'TestName'
    user1_password = 'TestPassword1234'


G = Globals
