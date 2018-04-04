from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from people.forms import UserProfileForm

UserModel = get_user_model()


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'people/user_profile.html'


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserProfileForm
    template_name = 'people/user_profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user_profile')
