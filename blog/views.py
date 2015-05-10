from django.shortcuts import render, get_object_or_404

from .models import Post


def list_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/list_posts.html', {'posts': posts})


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

