import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G


@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.usefixtures("load_checkpoint2")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("checkpoint_list.html", "/checkpoints/"),
        ("checkpoint_detail.html", "/checkpoint/TestCheckPoint1/"),
        ("checkpoint_detail.html", "/checkpoint/TestCheckPoint2/"),
    ])
def test_template_by_url_with_anonymous(client, template, url):
    """Test that template is reachable by using relative url address."""
    response = client.get(url, follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))


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
    assert bytes(
        f"""<iframe height="400px" width="400px" srcdoc=\'\n<!DOCTYPE HTML>\n<head>\n  <title>Point map</title>""",
        encoding=response.charset) in response.content


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
    assert bytes(f"Longitudinal: {G.checkpoint1_lon}", encoding=response.charset) in response.content
    assert bytes(f"Lateral: {G.checkpoint1_lat}", encoding=response.charset) in response.content
    # TODO: TEST IMAGE SOMEHOW...


