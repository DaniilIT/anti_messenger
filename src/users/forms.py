from django import forms
from django_registration.forms import RegistrationForm
from tinymce.widgets import TinyMCE

from .models import User


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=30, required=False)

    last_name = forms.CharField(label='Фамилия', max_length=30, required=False)

    avatar = forms.ImageField(
        label='Загрузите фото',
        required=False,
        widget=forms.FileInput
    )

    about_yourself = forms.CharField(
        label='Про себя',
        required=False,
        widget=TinyMCE()
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'about_yourself')
