from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render

from .forms import ProfileForm


class CustomPasswordResetView(PasswordResetView):
    subject_template_name = 'users/email/password_reset_subject.txt'
    html_email_template_name = 'users/email/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.request.session['reset_email'] = email
        return super().form_valid(form)


@login_required
def profile(request):
    form = ProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'users/profile.html', context)
