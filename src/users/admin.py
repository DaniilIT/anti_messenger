from datetime import timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from anti_messenger.settings import ACCOUNT_ACTIVATION_DAYS

from .models import User

admin.site.site_header = 'Anti-Messenger'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'last_login')
    actions = ('delete_inactive_users',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'preview_avatar', 'avatar', 'about_yourself')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('preview_avatar', 'last_login', 'date_joined')

    @admin.action(description='Удалить неактивных пользователей')
    def delete_inactive_users(self, request, queryset):
        """ Удалить всех неактивных пользователей, которые зарегистрировались более 7 дней назад.
        """
        several_days_ago = timezone.now() - timedelta(days=ACCOUNT_ACTIVATION_DAYS)
        queryset.objects.filter(is_active=False, date_joined__lte=several_days_ago).delete()

    @admin.display(description='предпросмотр')
    def preview_avatar(self, user):
        return format_html('<img src="{}" style="max-width: 256px;">', user.avatar.url)


admin.site.unregister(Group)
