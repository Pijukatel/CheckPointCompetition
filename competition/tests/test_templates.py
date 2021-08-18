import os

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from .globals_for_tests import G

template_folder = f"{G.APP_NAME}/templates/{G.APP_NAME}"
template_files = [os.path.join(template_folder, template)
                  for template in os.listdir(template_folder) if ".html" in template]


@pytest.mark.parametrize('template_file', template_files)
def test_template_extends_base(template_file):
    with open(template_file, "r") as f:
        assert '{% extends "base.html" %}' in f.read()


@pytest.mark.django_db
def test_base_template_context_for_anonymous(client):
    response = client.get(reverse("home"), follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "base.html")
    assert bytes('href="/accounts/login/"', response.charset) in response.content
    assert bytes('href="/accounts/register/"', response.charset) in response.content
    assert bytes('href="/accounts/user/"', response.charset) not in response.content
    assert bytes('href="/accounts/logout/"', response.charset) not in response.content
    assert bytes('href="/team/create/"', response.charset) not in response.content


@pytest.mark.usefixtures('load_registered_user1')
@pytest.mark.django_db
def test_base_template_context_for_logged_user_without_team(client_with_logged_user1):
    response = client_with_logged_user1.get(reverse("home"), follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "base.html")
    assert bytes('href="/accounts/user/"', response.charset) in response.content
    assert bytes('href="/accounts/logout/"', response.charset) in response.content
    assert bytes('href="/team/create/"', response.charset) in response.content
    assert bytes('href="/accounts/login/"', response.charset) not in response.content
    assert bytes('href="/accounts/register/"', response.charset) not in response.content


@pytest.mark.usefixtures('load_registered_user1_with_team1')
@pytest.mark.django_db
def test_base_template_context_for_logged_user_with_team(client_with_logged_user1):
    response = client_with_logged_user1.get(reverse("home"), follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "base.html")
    assert bytes('href="/accounts/user/"', response.charset) in response.content
    assert bytes('href="/accounts/logout/"', response.charset) in response.content
    assert bytes(f'href="/team/{G.team1_name}/"', response.charset) in response.content
    assert bytes('href="/team/create/"', response.charset) not in response.content
    assert bytes('href="/accounts/login/"', response.charset) not in response.content
    assert bytes('href="/accounts/register/"', response.charset) not in response.content


@pytest.mark.django_db
def test_base_template_side_bar_links(client):
    response = client.get(reverse("home"), follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "base.html")
    assert bytes('href="/accounts/users/"', response.charset) in response.content
    assert bytes('href="/teams/"', response.charset) in response.content
