from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView, TemplateView

from cfp.models import CallForPaper, PaperApplication

from .models import UserGroup, Vote


class AuthMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated():
            return False

        if not self.request.user.is_admin():
            return False

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


class ApplicationRateView(AuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))
        usergroup_id = int(request.POST.get('usergroup_id'))
        score = int(request.POST.get('score'))

        if score < 1 or score > 5:
            raise ValidationError("Invalid score")

        application = get_object_or_404(PaperApplication, pk=application_id)
        usergroup = get_object_or_404(UserGroup, pk=usergroup_id)

        # See if a vote already exists
        vote = Vote.objects.filter(
            user=request.user,
            usergroup=usergroup,
            application=application).first()

        if vote:
            vote.score = score
            vote.save()
        else:
            vote = Vote.objects.create(
                user=request.user,
                usergroup=usergroup,
                application=application,
                score=score,
            )

        return HttpResponse("You have voted successfully.")


class ApplicationUnrateView(AuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))
        usergroup_id = int(request.POST.get('usergroup_id'))

        application = get_object_or_404(PaperApplication, pk=application_id)
        usergroup = get_object_or_404(UserGroup, pk=usergroup_id)

        Vote.objects.filter(user=request.user, usergroup=usergroup, application=application).delete()

        return HttpResponse("You have unvoted successfully.")
