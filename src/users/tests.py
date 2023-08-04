from django.test import Client, TestCase
from django.urls import reverse

from .forms import CustomRegistrationForm, ProfileForm
from .models import User


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='testuser',
                password='testpassword'
            )

    def test_get_user_for_card(self):
        user = User.objects.get_user_for_card(self.user)
        self.assertEqual(user.messages_count, 0)


class FormTestCase(TestCase):
    def test_custom_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = CustomRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'avatar': None,
            'about_yourself': 'This is a test about me.'
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_main_page_view(self):
        response = self.client.get(reverse('main-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('theme-list'))

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('profile'))

    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, '<div class="bg-yellow-50 h-48', count=User.objects.count())
