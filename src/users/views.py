from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.db.models import Count, Q
from django.shortcuts import render
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
        print('D')
        if search_query := self.request.GET.get('search'):
            print(search_query)
            queryset = queryset.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        return queryset.order_by('-last_login')


@login_required
def profile(request):
    form = ProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'users/profile.html', context)
