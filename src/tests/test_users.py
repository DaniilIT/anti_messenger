import pytest
from django.db import IntegrityError
from django.urls import reverse


def test_main_page_view(client):
    response = client.get(reverse('main-page'))
    assert response.status_code == 200
    assert 'main_page.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_user(user_factory):
    user = user_factory.build(
        username='testuser',
        email='test@example.com',
    )
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'


@pytest.mark.django_db
def test_create_user_without_email(user_factory):
    with pytest.raises(IntegrityError):
        user_factory.create(email=None)


def test_login_view(client, test_user):
    response = client.post(reverse('login'), {
        'username': test_user.username,
        'password': 'test_password'
    })
    assert response.status_code == 302
    assert response.url == reverse('theme-list')


def test_profile_view(client, logged_user):
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    assert 'users/profile.html' in [t.name for t in response.templates]

    client.logout()
    response = client.get(reverse('profile'))
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('profile')


def test_user_list_view(client, logged_user):
    response = client.get(reverse('user-list'))
    assert response.status_code == 200
    assert 'users/user_list.html' in [t.name for t in response.templates]
    assert '<div class="bg-yellow-50 h-48' in response.content.decode()
