import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G

@pytest.mark.django_db
def test_view_map_template(client_with_logged_user1):
    response = client_with_logged_user1.get(f"/map/", follow=True)
    assertTemplateUsed(response, "/".join([G.APP_NAME, "competition_map.html"]))
