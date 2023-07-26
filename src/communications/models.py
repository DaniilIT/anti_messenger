import uuid

from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from PIL import Image
from tinymce import models as tinymce_models

from users.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего обновления', auto_now=True)

    class Meta:
        abstract = True


class Message(BaseModel):
    title = models.CharField('Название', max_length=150)
    picture = models.ImageField('Картинка', upload_to='pictures')
    generate_text = models.TextField('Сгенерированный текст', blank=True)
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE,
                              verbose_name='Тема', related_name='messages')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.picture.path) as picture:
            resize = (1920, 1080)
            picture.thumbnail(resize)
            picture.save(self.picture.path)

    def __str__(self):
        return self.title if len(self.title) <= 24 else self.title[:24] + '...'


class Theme(BaseModel):
    title = models.CharField('Название', max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='themes')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def get_absolute_url(self):
        return reverse('theme-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title if len(self.title) <= 24 else self.title[:24] + '...'


class Comment(BaseModel):
    text = tinymce_models.HTMLField('текст')
    message = models.ForeignKey('Message', on_delete=models.CASCADE,
                                verbose_name='Сообщение', related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        text = strip_tags(self.text)
        return text if len(text) <= 24 else text[:24] + '...'
