import pytest
from pytest_django.asserts import assertTemplateUsed
from .globals_for_tests import G
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def register_test_user(client, username='TestName', password='TestPassword1234'):
    response = client.post('/accounts/register/',
                           {'username': username,
                            'password1': password,
                            'password2': password},
                           follow=True)
    return response


@pytest.mark.parametrize(
    'template, url', [
        ('home.html', ''),
        ('register.html', '/accounts/register/')
    ])
def test_template_by_url_with_anonymous(client, template, url):
    """Test that template is reachable by using relative url address."""
    response = client.get(url, follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, template]))


@pytest.mark.django_db
def test_register_redirect(client):
    response = register_test_user(client)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'home.html']))


@pytest.mark.django_db
def test_register_user_created(client):
    username = 'TestName'
    register_test_user(client, username=username)
    user = User.objects.filter(username=username)
    assert user.exists()


@pytest.mark.django_db
def test_register_duplicated_user_denied(client):
    register_test_user(client)
    response = register_test_user(client)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'register.html']))
    assert isinstance(response.context_data['form'].errors['username'].data[0], ValidationError)
