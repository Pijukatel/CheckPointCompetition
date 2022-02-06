import html

import pytest

from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G


@pytest.mark.disable_default_time
@pytest.mark.usefixtures("in_countdown")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("home.html", ""),
        ("home.html", "/accounts/register/"),
        ("home.html", "/accounts/login/"),
        ("home.html", "/accounts/logout/"),
        ("home.html", "/accounts/user/"),
        ("home.html", "/accounts/users/"),
        ("home.html", "/accounts/user/delete/"),
        ("home.html", "/accounts/user/update/"),
        ("home.html", "/checkpoints/"),
        ("home.html", f"/checkpoints/{G.checkpoint1_name}"),
        ("home.html", "/point/photo-confirm/"),
        ("home.html", "/team/create/"),
        ("home.html", "/team/leave/"),
        ("home.html", f"/team/{G.team1_name}/"),
        ("home.html", f"/team/{G.team1_name}/update/"),
        ("home.html", f"/team/{G.team1_name}/delete/"),
        ("home.html", f"/team/{G.team1_name}/add_member/"),
        ("home.html", "/team/photo-confirm/"),
        ("home.html", "/teams/"),
    ])
def test_template_by_url_with_anonymous_require_login(client, template, url, far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))
    assert f"Competition will be open for registration: {far_future.isoformat()}" in html.unescape(
        response.content.decode(response.charset))
