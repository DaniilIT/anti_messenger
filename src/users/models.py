from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, Count, EmailField, ImageField
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tinymce.models import HTMLField


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        return super()._create_user(username, email, password, **extra_fields)

    def get_user_for_card(self, request_user, username=None):
        """ Получить пользователя с подсчитанным количеством его сообщений
        """
        username = username or request_user.username
        user = get_object_or_404(
            self.annotate(messages_count=Count('themes__messages')),
            pk=username
        )
        return user


class User(AbstractUser):
    # username - primary_key
    username = CharField(_('username'), max_length=150, primary_key=True, validators=[UnicodeUsernameValidator()],
                         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                         error_messages={'unique': _('A user with that username already exists.')})
    # email - unique
    email = EmailField(_('email address'), unique=True, help_text='Обязательное поле.',
                       error_messages={'unique': 'Пользователь с таким email уже существует.'})

    avatar = ImageField('Аватарка', default='avatars/default.png', upload_to='avatars')
    about_yourself = HTMLField('Про себя', blank=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            with Image.open(self.avatar.path) as avatar:
                resize = (256, 256)
                avatar.thumbnail(resize)
                avatar.save(self.avatar.path)
