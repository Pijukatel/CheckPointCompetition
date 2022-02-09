from datetime import datetime, timedelta
import pytz

COUNTDOWN = pytz.UTC.localize(datetime.now() - timedelta(seconds=3))
PRE_REGISTRATION = pytz.UTC.localize(datetime.now() - timedelta(seconds=2))
COMPETITION = pytz.UTC.localize(datetime.now() - timedelta(seconds=1))
ARCHIVED = pytz.UTC.localize(datetime.now() + timedelta(seconds=15))
