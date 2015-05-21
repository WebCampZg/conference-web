from django.shortcuts import render, get_object_or_404

from .models import Post


def list_posts(request):
    posts = Post.objects.all()

    ctx = {}
    ctx['posts'] = posts

    return render(request, 'blog/list_posts.html', ctx)


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

    ctx = {}
    ctx['post'] = post
    ctx['previous'] = previous
    ctx['next'] = next

    return render(request, 'blog/view_post.html', ctx)

