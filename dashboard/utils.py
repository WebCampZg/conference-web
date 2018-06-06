from collections import defaultdict
from django.db.models import Count


def get_votes_distribution(votes):
    counts = votes.order_by().values('score').annotate(count=Count('*'))

    distribution = defaultdict(lambda: 0)
    for c in counts:
        distribution[str(c['score'])] = c['count']

    return distribution
