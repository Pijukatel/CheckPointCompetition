from datetime import datetime, timedelta

COUNTDOWN = datetime.now() - timedelta(seconds=1)
PRE_REGISTRATION = datetime.now() + timedelta(seconds=5)
COMPETITION = datetime.now() + timedelta(seconds=10)
ARCHIVED = datetime.now() + timedelta(seconds=15)