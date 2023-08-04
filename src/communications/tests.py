from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from anti_messenger.settings import MEDIA_ROOT
from users.models import User

from .models import Comment, Message, Theme


class ThemeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_theme_list_view(self):
        response = self.client.get(reverse('theme-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communications/theme_list.html')

    def test_create_theme(self):
        response = self.client.post(
            reverse('theme-create'),
            {'title': 'Test Message'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Theme.objects.count(), 1)
        self.assertRedirects(response, reverse('message-list') + f'?theme={Theme.objects.first().id}')


class MessageViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.theme = Theme.objects.create(
            title='Test Theme',
            user=self.user
        )

    def tearDown(self):
        for message in Message.objects.all():
            img_path = MEDIA_ROOT / message.picture.name
            if img_path.exists():
                img_path.unlink()

    def test_message_list_view(self):
        response = self.client.get(reverse('message-list') + f'?theme={self.theme.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communications/message_list.html')

    def test_create_message(self):
        with open(MEDIA_ROOT / 'test_image.jpg', 'rb') as img:
            uploaded_img = SimpleUploadedFile('test_image.jpg', img.read())
            response = self.client.post(
                reverse('message-create') + f'?theme={self.theme.id}',
                {
                    'title': 'Test Message',
                    'picture': uploaded_img
                }
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        self.assertRedirects(response, reverse('comment-list') + f'?message={Message.objects.first().id}')


class CommentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.theme = Theme.objects.create(
            title='Test Theme',
            user=self.user
        )
        with open(MEDIA_ROOT / 'test_image.jpg', 'rb') as img:
            uploaded_img = SimpleUploadedFile('test_image.jpg', img.read())
            self.message = Message.objects.create(
                title='Test Message',
                picture=File(uploaded_img),
                theme=self.theme
            )

    def tearDown(self):
        for message in Message.objects.all():
            img_path = MEDIA_ROOT / message.picture.name
            if img_path.exists():
                img_path.unlink()

    def test_comment_list_view(self):
        response = self.client.get(reverse('comment-list') + f'?message={self.message.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communications/comment_list.html')

    def test_create_comment(self):
        response = self.client.post(
            reverse('comment-create') + f'?message={self.message.id}',
            {'text': 'Test Comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(response, reverse('comment-list') + f'?message={self.message.id}')
