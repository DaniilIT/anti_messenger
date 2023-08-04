import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from anti_messenger.settings import MEDIA_ROOT
from communications.models import Comment, Message, Theme


def test_theme_list_view(client, logged_user):
    response = client.get(reverse('theme-list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_theme(client, logged_user):
    response = client.post(
        reverse('theme-create'),
        {'title': 'Test Message'}
    )
    assert response.status_code == 302
    assert Theme.objects.count() == 1
    assert response.url == reverse('message-list') + f'?theme={Theme.objects.first().id}'


def test_message_list_view(client, logged_user, test_theme):
    response = client.get(reverse('message-list') + f'?theme={test_theme.id}')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_message(client, logged_user, test_theme):
    with open(MEDIA_ROOT / 'test_image.jpg', 'rb') as img:
        uploaded_img = SimpleUploadedFile('test_image.jpg', img.read())
        response = client.post(
            reverse('message-create') + f'?theme={test_theme.id}',
            {
                'title': 'Test Message',
                'picture': uploaded_img
            }
        )

    assert response.status_code == 302
    assert Message.objects.count() == 1
    assert response.url == reverse('comment-list') + f'?message={Message.objects.first().id}'


def test_comment_list_view(client, logged_user, test_message):
    response = client.get(reverse('comment-list') + f'?message={test_message.id}')
    assert response.status_code == 200


def test_create_comment(client, logged_user, test_message):
    response = client.post(
        reverse('comment-create') + f'?message={test_message.id}',
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert Comment.objects.count() == 1
    assert response.url == reverse('comment-list') + f'?message={test_message.id}'
