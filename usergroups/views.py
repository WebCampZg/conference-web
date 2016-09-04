from cfp.models import CallForPaper, PaperApplication
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, TemplateView


class AuthMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated():
            return False

        if not self.request.user.usergroup_set.exists():
            raise PermissionDenied("Must be a user group representative")

        return True


class DashboardView(AuthMixin, TemplateView):
    template_name = 'usergroups/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        ctx['cfps'] = CallForPaper.objects.order_by("-pk")
        return ctx


class CallForPapersView(AuthMixin, DetailView):
    model = CallForPaper
    template_name = 'usergroups/call_for_papers.html'

    def get_context_data(self, **kwargs):
        ctx = super(CallForPapersView, self).get_context_data(**kwargs)

        ctx['applications'] = (self.get_object().applications
            .prefetch_related('applicant', 'applicant__user', 'skill_level', 'talk')
            .order_by('pk'))

        return ctx


class ApplicationDetailView(AuthMixin, DetailView):
    model = PaperApplication
    template_name = 'usergroups/application.html'
    context_object_name = 'application'
