import pytest
from pytest_django.asserts import assertTemplateUsed, assertTemplateNotUsed
from .globals_for_tests import G


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_anonymous(client):
    """Test that template is reachable by using relative url address."""
    response = client.get("/checkpoint/TestCheckPoint1/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_detail.html"]))
    assertTemplateNotUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_anonymous(client):
    """Test that template is reachable by using relative url address."""
    response = client.get("/checkpoints/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_list.html"]))
    assertTemplateNotUsed(response, "/".join([G.APP_NAME, "checkpoint_list_confirmed_team.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_point2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_logged_user_with_confirmed_team(client_with_logged_user1):
    """Test that template is reachable by using relative url address."""
    response = client_with_logged_user1.get("/checkpoints/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_list_confirmed_team.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_point2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_logged_user_with_non_confirmed_team(client_with_logged_user1):
    """Test that template is reachable by using relative url address."""
    response = client_with_logged_user1.get("/checkpoints/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_list.html"]))
    assertTemplateNotUsed(response, "/".join([G.APP_NAME, "checkpoint_list_confirmed_team.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_point2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_logged_user_with_confirmed_team(client_with_logged_user1):
    """Test that template is reachable by using relative url address."""
    response = client_with_logged_user1.get("/checkpoint/TestCheckPoint1/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_detail.html"]))


@pytest.mark.usefixtures("load_point1")
@pytest.mark.usefixtures("load_point2")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.django_db
def test_checkpoint_list_templates_by_url_with_logged_user_with_non_confirmed_team(client_with_logged_user1):
    """Test that template is reachable by using relative url address."""
    response = client_with_logged_user1.get("/checkpoint/TestCheckPoint1/", follow=True)
    assertTemplateNotUsed(response, "/".join([G.APP_NAME, "components/checkpoint_detail_confirmed_team.html"]))
    assertTemplateUsed(response, "/".join([G.APP_NAME, "checkpoint_detail.html"]))


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.django_db
def test_checkpoints_list_view_contains_correct_names(client):
    response = client.get("/checkpoints/", follow=True)
    assert bytes(f"{G.checkpoint1_name}</a>", encoding=response.charset) in response.content
    assert bytes(f"{G.checkpoint2_name}</a>", encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.django_db
def test_checkpoints_list_view_contains_map(client):
    response = client.get("/checkpoints/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/map.html"]))


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.django_db
def test_checkpoints_list_view_map_contains_all_checkpoints(client):
    response = client.get("/checkpoints/", follow=True)
    assert bytes(f"OpenLayers.Geometry.Point( {G.checkpoint1_lon}, {G.checkpoint1_lat} )",
                 encoding=response.charset) in response.content
    assert bytes(f"OpenLayers.Geometry.Point( {G.checkpoint2_lon}, {G.checkpoint2_lat} )",
                 encoding=response.charset) in response.content


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
def test_checkpoint_detail_view_contains_correct_data(client):
    response = client.get("/checkpoint/TestCheckPoint1/", follow=True)
    assert bytes(f"Name: {G.checkpoint1_name}", encoding=response.charset) in response.content
    assert bytes(f"Description: {G.checkpoint1_description}", encoding=response.charset) in response.content
    assert bytes(f'Longitudinal: <span id="focusLon">{G.checkpoint1_lon}', encoding=response.charset) in response.content
    assert bytes(f'Lateral: <span id="focusLat">{G.checkpoint1_lat}', encoding=response.charset) in response.content
    # TODO: TEST IMAGE SOMEHOW...
