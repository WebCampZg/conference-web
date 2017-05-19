import pytest

from django.urls import reverse

from tests.factories import PostFactory


@pytest.mark.django_db
def test_list_view(client):
    posts = [PostFactory(), PostFactory(), PostFactory()]
    url = reverse('blog_list_posts')

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200

    for post in posts:
        assert post.title in content
        assert post.lead in content


@pytest.mark.django_db
def test_detail_view(client):
    post = PostFactory()
    url = reverse('blog_view_post', kwargs={"slug": post.slug})

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert post.title in content
    assert post.lead in content
    assert post.body in content
