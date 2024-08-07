from datetime import datetime
from typing import List, Dict, Any, Tuple, Set

import pytest
import pytz
from freezegun import freeze_time
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from ..models import UserPosition


def set_of_items_from_list_of_dicts(in_list: List[Dict[Any, Any]]) -> Set[Tuple[Any, ...]]:
    return {tuple(inner_dict.items()) for inner_dict in in_list}

def list_of_items_from_list_of_dicts(in_list: List[Dict[Any, Any]]) -> Set[Tuple[Any, ...]]:
    return [tuple(inner_dict.items()) for inner_dict in in_list]


@pytest.mark.django_db
@pytest.mark.parametrize("endpoint", ("current_user_pos",))
def test_api_endpoints_not_public(client, endpoint):
    """Only logged users can access API endpoints."""
    response = client.get(f"/api/{endpoint}/", follow=True)
    assert response.headers["content-type"] != "application/json"
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))


@pytest.mark.django_db
def test_points(client_with_logged_user1, load_4points_from_2_confiremed_teams_2checkpoints):
    response = client_with_logged_user1.get("/api/points/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [
        {"confirmed": False, "checkpoint_id": G.checkpoint1_name, "team_id": G.team1_name},
        {"confirmed": False, "checkpoint_id": G.checkpoint2_name, "team_id": G.team1_name},
        {"confirmed": False, "checkpoint_id": G.checkpoint1_name, "team_id": G.team2_name},
        {"confirmed": False, "checkpoint_id": G.checkpoint2_name, "team_id": G.team2_name}
    ]
    assert set_of_items_from_list_of_dicts(response.json()) == set_of_items_from_list_of_dicts(expected_data)


@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_teams(client_with_logged_user1):
    response = client_with_logged_user1.get("/api/teams/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [{'name': G.team1_name, 'confirmed': False}, {'name': G.team2_name, 'confirmed': False}]
    assert set_of_items_from_list_of_dicts(response.json()) == set_of_items_from_list_of_dicts(expected_data)


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_custom_position")
@pytest.mark.django_db
def test_user_positions(client_with_logged_user1):
    response = client_with_logged_user1.get("/api/user_positions/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [
        {'gps_lat': G.user1_lats[0], 'gps_lon': G.user1_lons[0], 'user': User.objects.get(username=G.user1_name).id},
        {'gps_lat': 0.0, 'gps_lon': 0.0, 'user': User.objects.get(username=G.user2_name).id}]
    assert set_of_items_from_list_of_dicts(response.json()) == set_of_items_from_list_of_dicts(expected_data)


@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
def test_checkpoint_positions(client_with_logged_user1):
    response = client_with_logged_user1.get("/api/checkpoint_positions/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [{'gps_lat': G.checkpoint1_lat, 'gps_lon': G.checkpoint1_lon, 'name': G.checkpoint1_name},
                     {'gps_lat': G.checkpoint2_lat, 'gps_lon': G.checkpoint2_lon, 'name': G.checkpoint2_name}]
    assert set_of_items_from_list_of_dicts(response.json()) == set_of_items_from_list_of_dicts(expected_data)


@pytest.mark.usefixtures("load_registered_user2_with_team2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_memberships(client_with_logged_user1):
    response = client_with_logged_user1.get("/api/memberships/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [{'user': User.objects.get(username=G.user1_name).id, 'team': G.team1_name},
                     {'user': User.objects.get(username=G.user2_name).id, 'team': G.team2_name}]
    assert set_of_items_from_list_of_dicts(response.json()) == set_of_items_from_list_of_dicts(expected_data)


@pytest.mark.parametrize("input_data", (
        {"gps_lat": G.user1_lats[1], "gps_lon": G.user1_lons[1]},
        {"gps_lat": G.user1_lats[1], "gps_lon": G.user1_lons[1], "user": 2},
        {"gps_lat": G.user1_lats[1], "gps_lon": G.user1_lons[1], "whatever": "a"}
))
@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_custom_position")
@pytest.mark.django_db
def test_user_positions_update(client_with_logged_user1, input_data):
    client_with_logged_user1.patch("/api/current_user_pos/", data=input_data, content_type="application/json")
    expected_positions = [
        {'gps_lat': G.user1_lats[1], 'gps_lon': G.user1_lons[1], 'user': User.objects.get(username=G.user1_name)},
        {'gps_lat': 0.0, 'gps_lon': 0.0, 'user': User.objects.get(username=G.user2_name)}]
    assert set(UserPosition.objects.all()) == {
        UserPosition(**expected_position) for expected_position in expected_positions}


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1_custom_position")
@pytest.mark.django_db
def test_user_positions_update_anonymoous(client):
    input_data = {"gps_lat": G.user1_lats[1], "gps_lon": G.user1_lons[1]}
    response = client.patch("/api/current_user_pos/", data=input_data, content_type="application/json", follow=True)
    assert response.headers["content-type"] != "application/json"
    assertTemplateUsed(response, "/".join([G.APP_NAME, "login.html"]))


@pytest.mark.usefixtures("load_registered_user2")
@pytest.mark.usefixtures("load_registered_user1")
@pytest.mark.django_db
def test_user(client_with_logged_user1):
    response = client_with_logged_user1.get("/api/user/", follow=True)
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {'id': User.objects.get(username=G.user1_name).id, 'username': G.user1_name}


@pytest.mark.django_db
def test_score(client_with_logged_user1, load_4points_from_2_confiremed_teams_2checkpoints):

    time1 = pytz.UTC.localize(datetime(year=2022, month=1, day=1, hour=1, minute=2))
    with freeze_time(time1):
        for point in load_4points_from_2_confiremed_teams_2checkpoints:
            if point.team_id == G.team1_name:
                point.confirmed = True
                point.visit_date = pytz.UTC.localize(datetime.now())
                point.save()

    response = client_with_logged_user1.get("/api/score/", follow=True)
    assert response.headers["content-type"] == "application/json"
    expected_data = [
        {"team": G.team1_name, "points": 2, "latest_updated_point": time1.strftime("%H:%M:%S")},
        {"team": G.team2_name, "points": 0, "latest_updated_point": "00:00:00"},
    ]
    assert list_of_items_from_list_of_dicts(response.json()) == list_of_items_from_list_of_dicts(expected_data)
