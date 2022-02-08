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
def test_template_in_countdown(client, template, url, far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))
    assert f"Competition will be open for registration: {far_future.isoformat()}" in html.unescape(
        response.content.decode(response.charset))


@pytest.mark.disable_default_time
@pytest.mark.usefixtures("in_pre_registration")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("home.html", ""),
        ("home.html", "/checkpoints/"),
        ("home.html", f"/checkpoints/{G.checkpoint1_name}"),
        ("home.html", "/point/photo-confirm/"),
    ])
def test_template_in_pre_registration_closed_views(client_with_logged_user1, template, url, far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client_with_logged_user1.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))
    assert f"Competition will start: {far_future.isoformat()}" in html.unescape(
        response.content.decode(response.charset))


@pytest.mark.disable_default_time
@pytest.mark.usefixtures("in_pre_registration")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("register.html", "/accounts/register/"),
        ("login.html", "/accounts/login/"),
        ("login.html", "/accounts/logout/"),
        ("user_detail.html", "/accounts/user/"),
        ("user_list.html", "/accounts/users/"),
        ("user_delete.html", "/accounts/user/delete/"),
        ("user_update.html", "/accounts/user/update/"),
        ("user_detail.html", "/team/leave/"),
        ("team_detail.html", f"/team/{G.team1_name}/"),
        ("team_update.html", f"/team/{G.team1_name}/update/"),
        ("team_delete.html", f"/team/{G.team1_name}/delete/"),
        ("team_add_member.html", f"/team/{G.team1_name}/add_member/"),
        ("login.html", "/team/photo-confirm/"),  # Redirect to staff
        ("team_list.html", "/teams/"),
    ])
def test_template_in_pre_registration_open_views(client_with_logged_user1, template, url, far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client_with_logged_user1.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))


@pytest.mark.disable_default_time
@pytest.mark.usefixtures("in_pre_registration")
@pytest.mark.usefixtures("load_registered_user1_with_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("team_create.html", "/team/create/"),  # Is actually without team.
        ("team_photo_confirmation.html", "/team/photo-confirm/"),
        ("photo_confirmation_empty.html", "/point/photo-confirm/"),
    ])
def test_template_in_pre_registration_open_views_by_staff(client_with_logged_user_staff, template, url, far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client_with_logged_user_staff.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))


@pytest.mark.disable_default_time
@pytest.mark.usefixtures("in_pre_registration")
@pytest.mark.usefixtures("load_registered_user1_with_confirmed_team1")
@pytest.mark.usefixtures("load_checkpoint1")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "template, url", [
        ("home.html", "/point/photo-confirm/"),
    ])
def test_template_in_pre_registration_open_views_by_staff_point_confirm(client_with_logged_user_staff, template, url,
                                                                        far_future):
    """Test that all endpoints are redirected to home in countdown stage."""
    response = client_with_logged_user_staff.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "/".join([G.APP_NAME, template]))
