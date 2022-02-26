from datetime import timedelta

import pytest
from freezegun import freeze_time

from ..models import Point
from ..score_board import get_teams_order
from ..settings import COMPETITION


@pytest.mark.django_db
def test_sorting_by_score(load_confirmed_teams_1_2_3_and_checkpoints_1_2_3):
    teams, checkpoints = load_confirmed_teams_1_2_3_and_checkpoints_1_2_3
    # Confirm 3 points of team 2
    # Confirm 1 points of team 1
    # Confirm 0 points of team 3
    confirmation_team2 = 0
    confirmation_team3 = 0
    points = Point.objects.all()
    for point in points:
        if point.team == teams[1] and confirmation_team3 < 3:
            confirmation_team3 += 1
            point.confirmed = True
        if point.team == teams[0] and confirmation_team2 < 1:
            point.confirmed = True
            confirmation_team2 += 1
        point.save()

    teams_order = get_teams_order()
    assert teams_order[0].team == teams[1].name
    assert teams_order[0].points == 3
    assert teams_order[1].team == teams[0].name
    assert teams_order[1].points == 1
    assert teams_order[2].team == teams[2].name
    assert teams_order[2].points == 0


@pytest.mark.django_db
def test_sorting_by_score_and_date(load_confirmed_teams_1_2_3_and_checkpoints_1_2_3):
    teams, checkpoints = load_confirmed_teams_1_2_3_and_checkpoints_1_2_3
    # Confirm 1 points of team 2 in t
    # Confirm 1 points of team 1 in t +1
    # Confirm 0 points of team 3
    confirmation_team2 = 0
    confirmation_team3 = 0
    with freeze_time(COMPETITION):
        point1 = Point.objects.filter(team=teams[1]).first()
        point1.confirmed = True
        point1.save()
    with freeze_time(COMPETITION + timedelta(seconds=1)):
        point2 = Point.objects.filter(team=teams[0]).first()
        point2.confirmed = True
        point2.save()

    teams_order = get_teams_order()
    assert teams_order[0].team == teams[1].name
    assert teams_order[0].points == 1
    assert teams_order[1].team == teams[0].name
    assert teams_order[1].points == 1
    assert teams_order[2].team == teams[2].name
    assert teams_order[2].points == 0
