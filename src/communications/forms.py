from django import forms

from .models import Comment, Message, Theme

# from tinymce.widgets import TinyMCE


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ('title',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'picture')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
