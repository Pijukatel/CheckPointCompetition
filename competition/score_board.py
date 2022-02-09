from datetime import datetime
import pytz
from typing import NamedTuple, List
from competition.models import Team, Point

from competition.models import Team


class TeamWithScore(NamedTuple):
    team: Team
    points: int
    latest_updated_point: datetime


def get_teams_order():
    """Sort teams by score descending and latest updated point ascending."""
    points = Point.objects.all()
    teams = Team.objects.all()
    teams_with_score: List[TeamWithScore] = []
    for team in teams:
        teams_with_score.append(get_team_with_score(team, points))
    return sorted(teams_with_score,
                  key=lambda team_with_score: (-team_with_score.points, team_with_score.latest_updated_point))


def get_team_with_score(team: Team, points: List[Point]):
    point_counter = 0
    latest_confirmed_point_time = pytz.UTC.localize(datetime(2000, 1, 1))  # Any old date from past.
    for point in points:
        if point.team == team and point.confirmed:
            point_counter += 1
            latest_confirmed_point_time = max(latest_confirmed_point_time, point.confirmation_date)
    return TeamWithScore(team, point_counter, latest_confirmed_point_time)
