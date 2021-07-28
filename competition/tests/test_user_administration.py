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


def login_test_user(client, username=G.user1_name, password=G.user1_password):
    response = client.post('/accounts/login/',
                           {'username': username,
                            'password': password},
                           follow=True)
    return response


@pytest.mark.parametrize(
    'template, url', [
        ('home.html', ''),
        ('register.html', '/accounts/register/'),
        ('login.html', '/accounts/login/')
    ])
def test_template_by_url_with_anonymous(client, template, url):
    """Test that template is reachable by using relative url address."""
    response = client.get(url, follow=True)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, template]))


@pytest.mark.django_db
def test_register_redirect(client):
    response = register_test_user(client)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'login.html']))


@pytest.mark.django_db
def test_register_user_created(client):
    register_test_user(client)
    user = User.objects.filter(username=G.user1_name)
    assert user.exists()


@pytest.mark.django_db
def test_register_duplicated_user_denied(client):
    register_test_user(client)
    response = register_test_user(client)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'register.html']))
    assert isinstance(response.context_data['form'].errors['username'].data[0], ValidationError)


@pytest.mark.usefixtures('load_registered_user')
@pytest.mark.django_db
def test_login_redirect(client):
    response = login_test_user(client)
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'user_detail.html']))


@pytest.mark.usefixtures('load_registered_user')
@pytest.mark.django_db
def test_login(client):
    login_test_user(client)
    response = client.get('/accounts/user/')
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'user_detail.html']))


@pytest.mark.usefixtures('load_registered_user')
@pytest.mark.django_db
def test_correct_user_detail(client):
    login_test_user(client)
    response = client.get('/accounts/user/')
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'user_detail.html']))


@pytest.mark.django_db
def test_nonexistent_login(client):
    response = login_test_user(client)
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'login.html']))
    assert b'Username or password is incorrect.' in response.content


@pytest.mark.usefixtures('load_registered_user')
@pytest.mark.django_db
def test_unauthorized_user(client):
    response = client.get('/accounts/user/', follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'login.html']))


@pytest.mark.usefixtures('load_registered_user')
@pytest.mark.django_db
def test_correct_user_detail(client_with_logged_user1):
    response = client_with_logged_user1.get('/accounts/user/')
    assert response.status_code == 200
    assertTemplateUsed(response, '/'.join([G.APP_NAME, 'user_detail.html']))
    assert bytes(f'{G.user1_name}', response.charset) in response.content