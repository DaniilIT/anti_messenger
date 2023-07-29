from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django_registration.backends.activation.views import RegistrationView

from .forms import CustomRegistrationForm, ProfileForm
from .models import User


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.request.session['reset_email'] = email
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    subject_template_name = 'users/email/password_reset_subject.txt'
    html_email_template_name = 'users/email/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.request.session['reset_email'] = email
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.annotate(messages_count=Count('themes__messages'))
        if search_query := self.request.GET.get('search'):
            queryset = queryset.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        return queryset.order_by('-last_login')


def main_page(request):
    return render(request, 'main_page.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect(reverse('theme-list'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'current_user': User.objects.get_user_for_card(request.user),
        'form': form,
    }
    return render(request, 'users/profile.html', context)
