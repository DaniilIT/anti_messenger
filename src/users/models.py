from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, EmailField, ImageField
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tinymce.models import HTMLField

from anti_messenger.settings import AVATAR_MAX_SIZE


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        return super()._create_user(username, email, password, **extra_fields)


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
            avatar = Image.open(self.avatar.path)

            if avatar.height > AVATAR_MAX_SIZE or avatar.width > AVATAR_MAX_SIZE:
                resize = (AVATAR_MAX_SIZE, AVATAR_MAX_SIZE)
                avatar.thumbnail(resize)
                avatar.save(self.avatar.path)
