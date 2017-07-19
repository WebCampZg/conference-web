from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from django.utils.timezone import get_current_timezone
from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory, ImageField

from blog.models import Post
from cfp.models import CallForPaper, Applicant, PaperApplication, AudienceSkillLevel
from people.models import User, TShirtSize
from events.models import Event, Ticket

timezone = get_current_timezone()


class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = LazyAttribute(lambda x: make_password('webcamp'))
    is_staff = False

    class Meta:
        model = User


class EventFactory(DjangoModelFactory):
    title = Faker('sentence')
    slug = Faker('slug')
    extended_title = Faker('sentence')
    tagline = Faker('sentence')
    begin_date = Faker('future_date')
    end_date = Faker('future_date')
    dates_text = Faker('sentence')

    class Meta:
        model = Event


class PostFactory(DjangoModelFactory):
    title = Faker('sentence')
    slug = LazyAttribute(lambda x: slugify(x.title)[0:50])
    author = SubFactory(UserFactory)
    is_sponsored = Faker('boolean')
    lead = Faker('text')
    body = Faker('text')

    class Meta:
        model = Post


class CallForPaperFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    title = Faker('sentence')
    description = Faker('sentence')
    announcement = Faker('sentence')
    begin_date = Faker('date')
    end_date = Faker('date')

    class Meta:
        model = CallForPaper


class ApplicantFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    about = Faker('text')
    biography = Faker('text')
    speaker_experience = Faker('text')
    image = ImageField()

    class Meta:
        model = Applicant


class TicketFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    user = SubFactory(UserFactory)
    tshirt_size = LazyAttribute(lambda x: TShirtSize.objects.order_by('?').first())
    category = 'Regular'
    code = Faker('random_number')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    country = Faker('country_code')
    company = Faker('company')
    promo_code = ''
    twitter = Faker('first_name')
    dietary_preferences = ''
    purchased_at = Faker('past_datetime', tzinfo=timezone)
    used_at = None

    class Meta:
        model = Ticket


class PaperApplicationFactory(DjangoModelFactory):
    cfp = SubFactory(CallForPaperFactory)
    applicant = SubFactory(ApplicantFactory)
    title = Faker('sentence')
    about = Faker('sentence')
    abstract = Faker('sentence')
    skill_level = LazyAttribute(lambda a: AudienceSkillLevel.objects.order_by('?').first())

    class Meta:
        model = PaperApplication
