from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, View

from users.models import User

from .forms import CommentForm, MessageForm, ThemeForm
from .models import Comment, Message, Theme
from .utils import ocr_core


class ErrorHandlingMixin(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))


class ThemeListView(LoginRequiredMixin, ListView):
    model = Theme
    # template_name = 'communications/theme_list.html'
    context_object_name = 'themes'
    extra_context = {'form': ThemeForm()}

    def get(self, request, *args, **kwargs):
        self.current_user = User.objects.get_user_for_card(
            request.user,
            username=self.request.GET.get('user')
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Theme.objects\
            .filter(user=self.current_user)\
            .annotate(messages_count=Count('messages'))\
            .order_by('-updated')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_user'] = self.current_user
        return ctx


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    # template_name = 'communications/theme_form.html'
    fields = ('title',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class MessageListView(LoginRequiredMixin, ErrorHandlingMixin, ListView):
    model = Message
    # template_name = 'communications/message_list.html'
    context_object_name = 'messages'
    extra_context = {'form': MessageForm()}

    def get(self, request, *args, **kwargs):
        theme_id = self.request.GET.get('theme')
        if theme_id is None:
            raise ValidationError('Missing "theme" parameter.', code='invalid_theme_id')

        self.current_theme = get_object_or_404(
            Theme.objects.select_related('user').annotate(messages_count=Count('messages')),
            pk=theme_id
        )
        self.current_user = User.objects.get_user_for_card(
            self.request.user,
            username=self.current_theme.user.username
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects\
            .filter(theme=self.current_theme)\
            .annotate(comments_count=Count('comments'))\
            .order_by('-updated')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_user'] = self.current_user
        ctx['current_theme'] = self.current_theme
        return ctx


class MessageCreateView(LoginRequiredMixin, ErrorHandlingMixin, CreateView):
    model = Message
    # template_name = 'communications/message_form.html'
    fields = ('title', 'picture')

    def form_valid(self, form):
        theme_id = self.request.GET.get('theme')
        if theme_id is None:
            raise ValidationError('Missing "theme" parameter.', code='invalid_theme_id')
        form.instance.theme = get_object_or_404(Theme, pk=theme_id)
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.generate_text = ocr_core(form.instance.picture.path)
        self.object.save()
        return response

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class CommentListView(ErrorHandlingMixin, ListView):
    model = Comment
    # template_name = 'communications/comment_list.html'
    context_object_name = 'comments'
    extra_context = {'form': CommentForm()}

    def get(self, request, *args, **kwargs):
        message_id = self.request.GET.get('message')
        if message_id is None:
            raise ValidationError('Missing "message" parameter.', code='invalid_message_id')

        self.current_message = get_object_or_404(
            Message.objects.select_related('theme', 'theme__user'),
            pk=message_id
        )
        self.current_theme = get_object_or_404(
            Theme.objects.annotate(messages_count=Count('messages')),
            pk=self.current_message.theme.pk
        )
        self.current_user = User.objects.get_user_for_card(
            self.request.user,
            username=self.current_message.theme.user.username
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects \
            .select_related('user') \
            .filter(message=self.current_message) \
            .order_by('-updated')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_user'] = self.current_user
        ctx['current_theme'] = self.current_theme
        ctx['current_message'] = self.current_message
        return ctx


class CommentCreateView(LoginRequiredMixin, ErrorHandlingMixin, CreateView):
    model = Comment
    # template_name = 'communications/comment_form.html'
    fields = ('text',)

    def form_valid(self, form):
        message_id = self.request.GET.get('message')
        if message_id is None:
            raise ValidationError('Missing "message" parameter.', code='invalid_message_id')

        form.instance.message = get_object_or_404(Message, pk=message_id)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])
