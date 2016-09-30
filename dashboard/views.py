from collections import Counter

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView, TemplateView, ListView

from cfp.models import CallForPaper, PaperApplication
from conferences.models import Ticket
from people.models import TShirtSize
from usergroups.models import UserGroup, Vote
from voting.models import Vote as CommunityVote, VoteToken

class ViewAuthMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated() and user.is_superuser


class VoteAuthMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated() and user.usergroup_set.count() > 0


class DashboardView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        ctx['cfps'] = CallForPaper.objects.order_by("-pk")
        return ctx


class CallForPapersView(ViewAuthMixin, DetailView):
    model = CallForPaper
    template_name = 'dashboard/call_for_papers.html'

    def get_context_data(self, **kwargs):
        ctx = super(CallForPapersView, self).get_context_data(**kwargs)

        ctx['applications'] = (self.get_object().applications
            .prefetch_related('applicant', 'applicant__user', 'skill_level', 'talk')
            .order_by('pk'))

        return ctx


class ApplicationDetailView(ViewAuthMixin, DetailView):
    model = PaperApplication
    template_name = 'dashboard/application.html'
    context_object_name = 'application'


class ApplicationRateView(VoteAuthMixin, View):

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


class ApplicationUnrateView(VoteAuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))
        usergroup_id = int(request.POST.get('usergroup_id'))

        application = get_object_or_404(PaperApplication, pk=application_id)
        usergroup = get_object_or_404(UserGroup, pk=usergroup_id)

        Vote.objects.filter(user=request.user, usergroup=usergroup, application=application).delete()

        return HttpResponse("You have unvoted successfully.")


class CommunityVoteView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/community-vote.html'

    def get_context_data(self, **kwargs):
        ctx = super(CommunityVoteView, self).get_context_data(**kwargs)

        ctx['vote_count'] = CommunityVote.objects.count()
        ctx['participants_voted'] = CommunityVote.objects.values('user').distinct().count()
        ctx['participants_total'] = VoteToken.objects.count()

        applications = (PaperApplication.objects
            .filter(exclude=False)
            .prefetch_related('votes', 'applicant', 'applicant__user', 'skill_level'))

        ctx['applications'] = sorted(applications, key=lambda x: x.votes_count, reverse=True)

        return ctx


class ConferenceTicketsView(ViewAuthMixin, ListView):
    model = Ticket
    template_name = 'dashboard/conference-tickets.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        ctx = super(ConferenceTicketsView, self).get_context_data(**kwargs)

        tickets = self.object_list.prefetch_related('tshirt_size')

        ctx['countries'] = self.most_common(tickets, lambda t: t.country)
        ctx['categories'] = self.most_common(tickets, lambda t: t.category)
        ctx['tshirts'] = self.tshirt_sizes(tickets)

        return ctx

    def tshirt_sizes(self, tickets):
        sizes = [t.tshirt_size_id for t in tickets]
        most_common = Counter(sizes).most_common()
        most_common_dict = dict(most_common)
        top_count = most_common[0][1]

        return [{
            "value": size.name,
            "count": most_common_dict.get(size.id, 0),
            "width": most_common_dict.get(size.id, 0) * 100 / top_count,
        } for size in TShirtSize.objects.all()]

    def most_common(self, tickets, value_fn):
        values = [value_fn(t) for t in tickets]
        most_common = Counter(values).most_common()

        return [{
            "value": x[0],
            "count": x[1],
            "width": (float(100 * x[1]) / most_common[0][1]), # for drawing progress bars
        } for x in most_common]
