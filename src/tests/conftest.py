import pytest
from pytest_factoryboy import register

from anti_messenger.settings import MEDIA_ROOT
from communications.models import Message

from .factories import (
    CommentFactory, MessageFactory, ThemeFactory, UserFactory,
)

register(UserFactory)
register(ThemeFactory)
register(MessageFactory)
register(CommentFactory)


@pytest.fixture
def test_user(db, user_factory):
    user = user_factory.create()  # build()
    return user


@pytest.fixture
def logged_user(db, client, test_user):
    client.login(username=test_user.username, password='test_password')
    return test_user


@pytest.fixture
def test_theme(db, theme_factory):
    theme = theme_factory.create()
    yield theme
    for message in Message.objects.all():
        img_path = MEDIA_ROOT / message.picture.name
        if img_path.exists():
            img_path.unlink()


@pytest.fixture
def test_message(db, message_factory):
    message = message_factory.create()
    return message


@pytest.fixture
def test_comment(db, comment_factory):
    comment = comment_factory.create()
    return comment
