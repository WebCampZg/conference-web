from braces.views._access import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from people.forms import UserProfileForm
from people.models import User


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'people/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user_profile')




