# -*- coding: utf-8 -*-

from random import shuffle

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse

from config.utils import get_active_event
from sponsors.choices import SPONSOR_TYPES
from sponsors.models import Sponsor
from usergroups.models import UserGroup


def navigation(request):
    return {
        "navigation": [
            ("Info", "/info/"),
            ("Venue", reverse("venue")),
            ("Timeline", "/timeline/"),
            # ("Workshops", "/workshops/"),
            ("Talks", reverse('talks_list_talks')),
            # ("Schedule", reverse('schedule_list_schedule')),
            ("News", reverse('blog_list_posts')),
            ("Jobs", reverse('jobs_list_jobs')),
            ("Code", "/code/"),
            ("Team", "/team/"),
        ]
    }


def sponsors(request):
    active = Sponsor.objects.active()
    sponsors = {t: active.filter(type=t).order_by('order') for t, _ in SPONSOR_TYPES}

    return {
        "sponsors": sponsors
    }


def usergroups(request):
    return {
        "usergroups": UserGroup.objects.order_by("name").filter(is_active=True)
    }


def event(request):
    event = get_active_event()

    return {
        'event': event,
        'cfp': event.get_cfp(),
    }


def webcamp(request):
    """Conference-related strings"""
    # TODO: move to database?

    abs_uri = request.build_absolute_uri

    return {
        "base_url": abs_uri('/').rstrip('/'),
        "links": {
            "sponsors_pdf": abs_uri('/media/wczg_2018_sponsors_brochure.pdf'),
            "volunteer_application": "http://goo.gl/forms/1LYfr3TEGs",
            "entrio": "https://www.entrio.hr/en/event/webcamp-zagreb-2017-4261",
            "facebook": "https://www.facebook.com/WebCampZagreb/",
            "twitter": "https://twitter.com/webcampzagreb/",
            "youtube": "https://www.youtube.com/user/WebCampZg",
            "linkedin": "https://www.linkedin.com/company-beta/6397140/",
            "github": "https://github.com/webcampzg",
            "google_plus": "https://plus.google.com/+WebcampzgOrgHR",
        },
        "webcamp": {
            "og_image": {
                "url": abs_uri(static("images/2018/og_image.png")),
                "width": 1200,
                "height": 630
            }
        }
    }


def team(request):
    team = [
        {
            "name": "Luka Mužinić",
            "image": "images/team/luka.jpg",
            "twitter": "lmuzinic",
            "job": "Pencil pusher"
        },
        {
            "name": "Martina Dumančić",
            "image": "images/team/martina.jpg",
            "twitter": "",
            "job": "Procurement",
        },
        {
            "name": "Filip Gjurin",
            "image": "images/team/filip.jpg",
            "twitter": "FilipGjurin",
            "job": "Graphic design",
        },
        {
            "name": "Ivan Habunek",
            "image": "images/team/ivan.jpg",
            "twitter": "ihabunek",
            "job": "Speakers & tech"
        },
        {
            "name": "Tomislav Capan",
            "image": "images/team/tomislav.jpg",
            "twitter": "tomislavcapan",
            "job": "Volunteers"
        },
        {
            "name": "Steve Tauber",
            "image": "images/team/steve.png",
            "twitter": "stevetauber",
            "job": "Master of ceremonies"
        },
        {
            "name": "Senko Rašić",
            "image": "images/team/senko.jpg",
            "twitter": "senkorasic",
            "job": "Beloved leader"
        },
        {
            "name": "Elizabeth Salazar",
            "image": "images/team/elizabeth.jpg",
            "twitter": "",
            "job": "Master of ceremonies"
        },
        {
            "name": "Miro Svrtan",
            "image": "images/team/miro.png",
            "twitter": "msvrtan",
            "job": "Workshops"
        },
        {
            "name": "Goran Jurić",
            "image": "images/team/goran.jpg",
            "twitter": "goran_juric",
            "job": "Workshops"
        },
        {
            "name": "Zoran Antolović",
            "image": "images/team/zoka.jpg",
            "twitter": "zoran_antolovic",
            "job": "Venue"
        },
    ]

    committee = [
        {
            "name": "Emanuel Blagonić",
            "image": "images/team/emanuel.png",
            "twitter": "eblagonic",
        },
        {
            "name": "Goran Jurić",
            "image": "images/team/goran.jpg",
            "twitter": "goran_juric",
        },
        {
            "name": "Saša Jurić",
            "image": "images/team/sasa.png",
            "twitter": "sasajuric",
        },
        {
            "name": "Neven Munđar",
            "image": "images/team/neven.jpg",
            "twitter": "nmundar",
        },
        {
            "name": "Andrea Knez Karačić",
            "image": "images/team/andrea.jpg",
            "twitter": "CodeWithCream",
        },
        {
            "name": "Ivan Čurić",
            "image": "images/team/ivan_curic.jpg",
            "twitter": "_baxuz",
        },
        {
            "name": "Davor Tomić",
            "image": "images/team/davor_tomic.jpg",
            "twitter": "davortomic",
        },
        {
            "name": "Slaven Tomac",
            "image": "images/team/slaven.png",
            "twitter": "slaventomac",
        },
    ]

    shuffle(team)
    shuffle(committee)

    return {
        "team": team,
        "committee": committee,
    }
