from cfp.models import CallForPaper
from django.core.management.base import BaseCommand
from django.db.models import StdDev, Count, Avg


class Command(BaseCommand):
    help = ('Dumps a list of applications with scoring info, ready to be '
            'copy/pasted into a google drive spreadsheet.')

    def add_arguments(self, parser):
        parser.add_argument('cfp_id', type=int)

    def dump_application(self, application):
        user = application.applicant.user

        track = None
        for label in application.labels.all():
            if label.name.startswith("Track: "):
                track = label.name[7:]
                break

        parts = [
            application.pk,
            user.full_name,
            application.title,
            application.type,
            application.skill_level.name,
            user.tshirt_size.name[0],  # sex
            "✈" if application.travel_expenses_required else None,
            "🛏" if application.accomodation_required else None,
            application.score_count,
            round(application.score_average, 1) if application.score_average else None,
            round(application.score_stddev, 1) if application.score_stddev else None,
            track,
        ]

        print("\t".join(str(p) if p else "" for p in parts))

    def handle(self, *args, **options):
        cfp = CallForPaper.objects.get(pk=options.get('cfp_id'))

        applications = (cfp.applications.talks()
            .prefetch_related('applicant__user__tshirt_size', 'skill_level', 'labels')
            .annotate(score_count=Count('committee_votes'))
            .annotate(score_average=Avg('committee_votes__score'))
            .annotate(score_stddev=StdDev('committee_votes__score'))
            .order_by('created_at'))

        for application in applications:
            self.dump_application(application)
