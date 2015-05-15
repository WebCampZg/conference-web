from django.shortcuts import render, get_object_or_404

from sponsors.models import Sponsor
from sponsors.choices import SPONSOR_TYPES
from .models import Post


def get_sponsors():
    diamond_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.DIAMOND)
    track_sposors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.TRACK)
    standard_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.STANDARD)
    supporter_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.SUPPORTER)
    return {'diamond_sponsors': diamond_sponsors,
            'track_sponsors': track_sposors,
            'standard_sponsors': standard_sponsors,
            'supporter_sponsors': supporter_sponsors}


def list_posts(request):
    sponsors = get_sponsors()
    posts = Post.objects.all()

    ctx = {}
    ctx['posts'] = posts
    ctx.update(sponsors)

    return render(request, 'blog/list_posts.html', ctx)


def view_post(request, slug):
    sponsors = get_sponsors()
    post = get_object_or_404(Post, slug=slug)
    try:
        previous = Post.get_previous_by_created_at(post)
    except Post.DoesNotExist:
        previous = None

    try:
        next = Post.get_next_by_created_at(post)
    except Post.DoesNotExist:
        next = None

    ctx = {}
    ctx['post'] = post
    ctx['previous'] = previous
    ctx['next'] = next
    ctx.update(sponsors)

    return render(request, 'blog/view_post.html', ctx)

