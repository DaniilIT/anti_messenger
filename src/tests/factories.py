from pathlib import Path

import factory
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile

from communications.models import Comment, Message, Theme
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')  # fake.name()
    email = factory.Sequence(lambda n: f'user_{n}@example.com')  # fake.email()
    password = make_password('test_password')  # fake.password()


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Theme

    title = factory.Faker('word')  # fake.word()
    user = factory.SubFactory(UserFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    title = factory.Faker('word')  # fake.word()
    picture = SimpleUploadedFile(
        name='test_image.jpg',
        content=open(Path(__file__).resolve().parent / 'test_image.jpg', 'rb').read(),
        content_type='image/jpeg'
    )
    theme = factory.SubFactory(ThemeFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('text')  # fake.text()
    message = factory.SubFactory(MessageFactory)
    user = factory.SubFactory(UserFactory)
