from django.db import transaction
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from people.models import User


class Command(BaseCommand):
    help = "Deletes all users which are not staff, not in voting committee and don't have any applications."

    def handle(self, *args, **options):

        users = (User.objects
            .filter(is_staff=False)
            .filter(applicant__isnull=True))

        committee = Group.objects.get(name='TalkCommittee').user_set.all()
        users = users.difference(committee)

        # Modles which are expected to be cascaded when deleting
        ok_to_delete = {
            'account.EmailAddress',
            'account.EmailConfirmation',
            'people.User',
        }

        with transaction.atomic():
            for u in users:
                print(f"Deleting {u.email}")
                count, values = u.delete()

                # Check only expected models were cascaded
                deleted = set({k: v for k, v in values.items() if v > 0}.keys())
                diff = deleted.difference(ok_to_delete)
                if diff:
                    print("Deleted: {deleted}")
                    raise ValueError(f"Unexpected deletions: {diff}")
