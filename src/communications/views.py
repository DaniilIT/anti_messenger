from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, View

from users.models import User

from .models import Message, Theme
from .utils import ocr_core


class ErrorHandlingMixin(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))


class ThemeListView(ErrorHandlingMixin, ListView):
    model = Theme
    # template_name = 'communications/theme_list.html'
    context_object_name = 'themes'

    def get_queryset(self):
        username = self.request.GET.get('user')
        if username is None:
            raise ValidationError('Missing "user" parameter.', code='invalid_username')
        user = get_object_or_404(User, pk=username)
        return Theme.objects.filter(user=user).order_by('-updated')


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    # template_name = 'communications/theme_form.html'
    fields = ('title',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['title'] = News.objects.filter(pk=self.kwargs['pk']).first()
        # ctx['title'] = 'Добавление статьи'
        return ctx


class ThemeDetailView(LoginRequiredMixin, DetailView):
    model = Theme
    # template_name = 'communications/theme_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['title'] = Course.objects.filter(slug=self.kwargs['slug']).first()
        # ctx['lessons'] = Lesson.objects.filter(course=ctx['title']).order_by('number')
        return ctx


class MessageListView(ErrorHandlingMixin, ListView):
    model = Message
    # template_name = 'communications/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        theme_id = self.request.GET.get('theme')
        if theme_id is None:
            raise ValidationError('Missing "theme" parameter.', code='invalid_theme_id')
        theme = get_object_or_404(Theme, pk=theme_id)
        return Message.objects.filter(theme=theme).order_by('-updated')


class MessageCreateView(LoginRequiredMixin, ErrorHandlingMixin, CreateView):
    model = Message
    # template_name = 'Communications/message_form.html'
    fields = ('title', 'picture')

    def form_valid(self, form):
        theme_id = self.request.GET.get('theme')
        if theme_id is None:
            raise ValidationError('Missing "theme" parameter.', code='invalid_theme_id')
        form.instance.theme = get_object_or_404(Theme, pk=theme_id)
        form.instance.title = 'название'
        form.save()
        form.instance.generate_text = ocr_core(form.instance.picture.path)
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    # template_name = 'communications/message_detail.html'
