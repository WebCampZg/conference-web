from django.shortcuts import render, get_object_or_404

from sponsors.models import Sponsor
from sponsors.choices import SPONSOR_TYPES
from .models import Post


def list_posts(request):
    diamond_sponsors = Sponsor.objects.filter(is_active=True).filter(type=SPONSOR_TYPES.DIAMOND)
    track_sposors = Sponsor.objects.filter(is_active=True).filter(type=SPONSOR_TYPES.TRACK)
    standard_sponsors = Sponsor.objects.filter(is_active=True).filter(type=SPONSOR_TYPES.STANDARD)
    supporter_sponsors = Sponsor.objects.filter(is_active=True).filter(type=SPONSOR_TYPES.SUPPORTER)
    posts = Post.objects.all()
    return render(request, 'blog/list_posts.html', {
        'posts': posts,
        'diamond_sponsors': diamond_sponsors,
        'track_sponsors': track_sposors,
        'standard_sponsors': standard_sponsors,
        'supporter_sponsors': supporter_sponsors})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try:
        previous = Post.get_previous_by_created_at(post)
    except Post.DoesNotExist:
        previous = None

    try:
        next = Post.get_next_by_created_at(post)
    except Post.DoesNotExist:
        next = None

    return render(request, 'blog/view_post.html', {
        'post': post,
        'previous': previous,
        'next': next})

