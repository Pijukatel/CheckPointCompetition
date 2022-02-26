import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G

@pytest.mark.django_db
def test_view_base_map_template(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/map_base/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "components/map_base.html"]))


@pytest.mark.django_db
def test_base_map_embeddable(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/map_base/", follow=True)
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
