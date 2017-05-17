import factory

from django.contrib.auth.hashers import make_password
from django.utils.text import slugify

from blog.models import Post
from cfp.models import CallForPaper, Applicant
from people.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.LazyAttribute(lambda x: make_password('webcamp'))
    is_staff = False

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.LazyAttribute(lambda x: slugify(x.title)[0:50])
    author = factory.LazyAttribute(lambda x: UserFactory())
    is_sponsored = factory.Faker('boolean')
    lead = factory.Faker('text')
    body = factory.Faker('text')

    class Meta:
        model = Post


class CallForPaperFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    announcement = factory.Faker('sentence')
    begin_date = factory.Faker('date')
    end_date = factory.Faker('date')

    class Meta:
        model = CallForPaper


class ApplicantFactory(factory.django.DjangoModelFactory):
    user = factory.LazyAttribute(lambda x: UserFactory())
    about = factory.Faker('text')
    biography = factory.Faker('text')
    speaker_experience = factory.Faker('text')
    image = factory.django.ImageField()

    class Meta:
        model = Applicant
