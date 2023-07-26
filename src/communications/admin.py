from django.contrib import admin
from django.utils.html import format_html

from .models import Comment, Message, Theme


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'theme', 'created')
    list_display_links = ('id', 'title')
    ordering = ('updated',)
    search_fields = ('title',)
    list_filter = ('theme', 'created')

    fields = ('title', 'preview_picture', 'picture', 'generate_text', 'theme', 'theme_user', 'updated', 'created')
    raw_id_fields = ('theme',)
    readonly_fields = ('preview_picture', 'theme_user', 'updated', 'created')

    @admin.display(description='предпросмотр')
    def preview_picture(self, message):
        return format_html('<img src="{}" style="max-width: 256px;">', message.picture.url)

    @admin.display(description='автор')
    def theme_user(self, message):
        return message.theme.user.username


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created')
    list_display_links = ('id', 'title')
    ordering = ('updated',)
    search_fields = ('title',)
    list_filter = ('created',)

    raw_id_fields = ('user',)
    readonly_fields = ('updated', 'created')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'message')
    search_fields = ('text',)
    list_filter = ('created',)
    ordering = ('updated',)

    raw_id_fields = ('message', 'user')
    readonly_fields = ('updated', 'created')
