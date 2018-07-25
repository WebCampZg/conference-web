import datetime
import statistics

from collections import Counter, defaultdict
from itertools import groupby

from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ValidationError, PermissionDenied
from django.urls import reverse
from django.db.models import Count, Q, Avg, StdDev
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from cfp.models import CallForPaper, PaperApplication, Applicant
from dashboard.forms import CommentForm
from dashboard.models import Comment, Vote as CommitteeVote
from dashboard.utils import get_votes_distribution
from events.models import Event, Ticket
from people.models import TShirtSize, User
from voting.models import CommunityVote


class ViewAuthMixin(AccessMixin):
    """Allow access to admins and people on the talk committee"""

    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())

        if not (user.is_superuser or user.is_talk_committee_member()):
            raise PermissionDenied("Only admins and talk committee members have dashboard access.")

        return super().dispatch(request, *args, **kwargs)


class VoteAuthMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_talk_committee_member()


class DashboardView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        ctx['events'] = Event.objects.order_by("-pk")
        return ctx


class EventDetailView(ViewAuthMixin, DetailView):
    model = Event
    template_name = 'dashboard/event.html'
    pk_url_kwarg = 'event_id'


class CallForPapersView(ViewAuthMixin, DetailView):
    model = CallForPaper
    template_name = 'dashboard/call_for_papers.html'

    def get_durations(self, applications):
        durations = (applications
            .order_by()
            .values('duration')
            .annotate(count=Count('*')))

        return [["{} min".format(d['duration']), d['count']] for d in durations]

    def get_sexes(self, applications):
        sexes = (applications
            .order_by()
            .values('applicant__user__tshirt_size__name')
            .annotate(count=Count('*')))

        sexes_counts = defaultdict(lambda: 0)
        for s in sexes:
            key = s['applicant__user__tshirt_size__name'].split()[0]
            sexes_counts[key] += s['count']

        return [[k, v] for k, v in sexes_counts.items()]

    def get_levels(self, applications):
        levels = (applications
            .order_by()
            .values('skill_level__name')
            .annotate(count=Count('*')))

        return [[l['skill_level__name'], l['count']] for l in levels]

    def get_context_data(self, **kwargs):
        ctx = super(CallForPapersView, self).get_context_data(**kwargs)

        applications = (self.get_object().applications
            .prefetch_related('applicant', 'applicant__user', 'skill_level', 'talk')
            .order_by('pk'))
        application_count = applications.count()

        votes = self.request.user.committee_votes.filter(application__cfp=self.object)
        vote_count = votes.count()

        rated_percentage = 100 * vote_count / application_count \
            if application_count else None

        average_score = sum(v.score for v in votes) / vote_count \
            if vote_count else None

        ctx.update({
            "applications": applications,
            "votes": {v.application_id: v.score for v in votes},
            "vote_count": vote_count,
            "application_count": application_count,
            "rated_percentage": rated_percentage,
            "average_score": average_score,
            "distribution": get_votes_distribution(votes),
            "durations": self.get_durations(applications),
            "sexes": self.get_sexes(applications),
            "levels": self.get_levels(applications),
        })

        return ctx


class ApplicationDetailView(ViewAuthMixin, DetailView):
    model = PaperApplication
    template_name = 'dashboard/application.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        application = self.get_object()
        user = self.request.user
        vote = CommitteeVote.objects.filter(user=user, application=application).first()

        comments = (application.comments
            .exclude(Q(is_private=True) & ~Q(author=user))  # Hide other users private comments
            .order_by("created_at")
            .prefetch_related('author'))

        other_applications = (application.applicant.applications
            .exclude(pk=application.pk)
            .order_by('cfp__event'))

        committee_votes = application.committee_votes.order_by('user__first_name')
        aggregates = committee_votes.aggregate(
            avg=Avg('score'),
            stdev=StdDev('score'),
            count=Count('*'),
        )

        ctx = super(ApplicationDetailView, self).get_context_data(**kwargs)
        ctx.update({
            "comments": comments,
            "allow_voting": user.is_talk_committee_member,
            "score": vote.score if vote else None,
            "other_applications": other_applications,
            "committee_votes": committee_votes,
            "committee_votes_avg": aggregates['avg'],
            "committee_votes_stdev": aggregates['stdev'],
            "committee_votes_count": aggregates['count'],
        })
        return ctx


class ApplicantDetailView(ViewAuthMixin, DetailView):
    model = Applicant
    template_name = 'dashboard/applicant.html'

    def get_context_data(self, **kwargs):
        applicant = self.get_object()
        applications = applicant.applications.order_by("-created_at")

        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "applications": applications,
        })
        return ctx


class ApplicationRateView(VoteAuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))
        score = int(request.POST.get('score'))

        if score < 1 or score > 5:
            raise ValidationError("Invalid score")

        application = get_object_or_404(PaperApplication, pk=application_id)

        obj, created = CommitteeVote.objects.update_or_create(
            user=request.user, application=application, defaults={"score": score})

        return HttpResponse(status=201 if created else 200)


class ApplicationUnrateView(VoteAuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))

        application = get_object_or_404(PaperApplication, pk=application_id)

        CommitteeVote.objects.filter(user=request.user, application=application).delete()

        return HttpResponse(status=204)


class CommunityVoteView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/community-vote.html'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs.get('event_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CommunityVoteView, self).get_context_data(**kwargs)

        votes = (CommunityVote.objects
            .filter(application__cfp__event=self.event)
            .order_by('-created_at')
            .prefetch_related('ticket'))

        votes_by_application = defaultdict(list)
        for vote in votes:
            votes_by_application[vote.application_id].append(vote)

        applications = (self.event.applications
            .filter(pk__in=votes_by_application.keys())
            .prefetch_related('applicant__user', 'skill_level'))

        # Sort by vote count + add votes
        applications = sorted(applications, key=lambda a: len(votes_by_application.get(a.pk)), reverse=True)
        applications = [(a, votes_by_application.get(a.pk)) for a in applications]

        ctx['event'] = self.event
        ctx['applications'] = applications
        ctx['vote_count'] = votes.count()
        ctx['participants_voted'] = votes.values('ticket').distinct().count()
        ctx['participants_total'] = self.event.tickets.count()

        return ctx


class EventTicketsView(ViewAuthMixin, ListView):
    model = Ticket
    template_name = 'dashboard/event-tickets.html'
    context_object_name = 'tickets'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs.get('event_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(event=self.event)

    def get_context_data(self, **kwargs):
        ctx = super(EventTicketsView, self).get_context_data(**kwargs)

        tickets = self.object_list.prefetch_related('tshirt_size').order_by('purchased_at')

        if tickets:
            ctx['countries'] = self.most_common(tickets, lambda t: t.country)
            ctx['categories'] = self.most_common(tickets, lambda t: t.short_category)
            ctx['tshirts'] = self.tshirt_sizes(tickets)
            ctx['tickets_by_date'] = self.tickets_by_date(tickets)

        ctx['event'] = self.event
        ctx['tickets'] = tickets

        return ctx

    def date_range(self, start, end):
        dates = []
        date = start
        while date <= end:
            dates.append(date)
            date += datetime.timedelta(days=1)
        return dates

    def tickets_by_date(self, tickets):
        groups = groupby(tickets, lambda t: t.purchased_at.date())
        tickets_by_date = {k: len(list(v)) for k, v in groups}

        # Create a list of all dates from the first ticket bought until today
        start_date = min(tickets_by_date.keys())
        end_date = min(self.event.end_date, datetime.date.today())
        dates = self.date_range(start_date, end_date)

        return [(date, tickets_by_date.get(date, 0)) for date in dates]

    def tshirt_sizes(self, tickets):
        sizes = [t.tshirt_size_id for t in tickets]
        most_common = Counter(sizes).most_common()
        most_common_dict = dict(most_common)
        top_count = most_common[0][1]
        total = tickets.count()

        return [{
            "value": size.name,
            "perc": round(100 * most_common_dict.get(size.id, 0) / total, 1) if total else None,
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


class BaseCommentEditView(ViewAuthMixin, ModelFormMixin, ProcessFormView):
    model = Comment
    form_class = CommentForm
    template_name = 'dashboard/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.application = PaperApplication.objects.get(pk=self.kwargs.get('application_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "application": self.application
        })
        return ctx

    def get_success_url(self):
        return reverse("dashboard:application_detail", kwargs={"pk": self.application.pk})


class CommentCreateView(BaseCommentEditView, CreateView):
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.application = self.application
        comment.author = self.request.user
        comment.save()

        return HttpResponseRedirect(self.get_success_url())


class CommentUpdateView(BaseCommentEditView, UpdateView):
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class CommentDeleteView(BaseCommentEditView, DeleteView):
    template_name = 'dashboard/comment_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ScoringView(ViewAuthMixin, DetailView):
    model = CallForPaper
    template_name = 'dashboard/scoring.html'

    def get_voter_stats(self, voter, application_count):
        votes = voter.committee_votes.filter(application__cfp=self.object)
        vote_count = votes.count()
        average = votes.aggregate(avg=Avg('score'))['avg']
        percentage = 100 * vote_count / application_count

        return {
            'full_name': voter.full_name,
            'initials': voter.initials,
            'count': vote_count,
            'total': application_count,
            'percentage': percentage,
            'average': average,
            'distribution': get_votes_distribution(votes),
        }

    def get_voters_with_stats(self, voters, application_count):
        return [self.get_voter_stats(v, application_count) for v in voters]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        voter_ids = (
            CommitteeVote.objects
                         .filter(application__cfp=self.object)
                         .values_list('user_id', flat=True)
                         .distinct())

        voters = User.objects.filter(pk__in=voter_ids).order_by('first_name')

        applications = (self.object.applications
                            .prefetch_related('applicant', 'applicant__user',
                                              'skill_level', 'talk', 'committee_votes')
                            .annotate(vote_count=Count('committee_votes'))
                            .order_by('pk'))

        for application in applications:
            application.processed_votes = []

            app_votes = application.committee_votes.all()
            for voter in voters:
                user_votes = [v for v in app_votes if v.user_id == voter.pk]
                application.processed_votes.append((
                    voter,
                    user_votes[0].score if user_votes else None,
                ))

            scores = [v.score for v in app_votes]
            application.mean = statistics.mean(scores) if scores else None
            application.stdev = statistics.stdev(scores) if len(scores) > 1 else None

        application_count = applications.count()

        ctx.update({
            "applications": applications,
            "voters": self.get_voters_with_stats(voters, application_count),
        })

        return ctx
