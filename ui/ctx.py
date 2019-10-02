# -*- coding: utf-8 -*-

from os.path import getmtime, abspath, join, dirname
from random import shuffle

from django.templatetags.static import static
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
            ("Workshops", reverse('workshops_list_workshops')),
            ("Talks", reverse('talks_list_talks')),
            ("Schedule", reverse('schedule_list_schedule')),
            ("News", reverse('blog_list_posts')),
            ("Jobs", reverse('jobs_list_jobs')),
            ("Code", "/code/"),
            ("Team", "/team/"),
        ]
    }


def footer_links(request):
    return {
        "footer_links": [
            ("Info", "/info/"),
            ("Venue", reverse("venue")),
            ("Timeline", "/timeline/"),
            # ("Tickets", "/tickets/"),
            ("Workshops", reverse('workshops_list_workshops')),
            ("Talks", reverse('talks_list_talks')),
            ("Schedule", reverse('schedule_list_schedule')),
            ("News", reverse('blog_list_posts')),
            ("Jobs", reverse('jobs_list_jobs')),
            ("Code", "/code/"),
            ("Team", "/team/"),
        ]
    }


def sponsors(request):
    active = Sponsor.objects.active().order_by('order')
    sponsors = {
        type: [s for s in active if s.type == type]
        for type, _ in SPONSOR_TYPES
    }

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
            "sponsors_pdf": abs_uri('/media/wczg_2019_sponsors_brochure.pdf'),
            "volunteer_application": "http://goo.gl/forms/1LYfr3TEGs",
            "entrio": "https://www.entrio.hr/en/event/webcamp-zagreb-2017-4261",
            "facebook": "https://www.facebook.com/WebCampZagreb/",
            "twitter": "https://twitter.com/webcampzagreb/",
            "youtube": "https://www.youtube.com/user/WebCampZg",
            "linkedin": "https://www.linkedin.com/company-beta/6397140/",
            "github": "https://github.com/webcampzg",
        },
        "webcamp": {
            "og_image": {
                "url": abs_uri(static("images/2019/og_image.png")),
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
            "name": "Ivan Habunek",
            "image": "images/team/ivan.jpg",
            "twitter": "ihabunek",
            "job": "Tech"
        },
        {
            "name": "Senko Rašić",
            "image": "images/team/senko.jpg",
            "twitter": "senkorasic",
            "job": "Beloved leader"
        },
        {
            "name": "Miro Svrtan",
            "image": "images/team/miro.png",
            "twitter": "msvrtan",
            "job": "Workshops"
        },
        {
            "name": "Tomo Šala",
            "image": "images/team/tomo.jpg",
            "twitter": "HcsOmot",
            "job": "Workshops"
        },
        {
            "name": "Zoran Antolović",
            "image": "images/team/zoka.jpg",
            "twitter": "zoran_antolovic",
            "job": "Venue"
        },
        {
            "name": "Maja Trepšić",
            "image": "images/team/maja.jpg",
            "twitter": "",
            "job": "Keynotes & Committee"
        },
        {
            "name": "Stanko Krtalić",
            "image": "images/team/stanko.jpg",
            "twitter": "monorkin",
            "job": "Speakers"
        },
    ]

    committee = [
        {
            "name": "Maja Trepšić",
            "image": "images/team/maja.jpg",
            "twitter": "",
        },
        {
            "name": "Stanko Krtalić",
            "image": "images/team/stanko.jpg",
            "twitter": "monorkin",
        },
        {
            "name": "Emanuel Blagonić",
            "image": "images/team/emanuel.png",
            "twitter": "eblagonic",
        },
        {
            "name": "Nela Dunato",
            "image": "images/team/nela.jpg",
            "twitter": "nelchee",
        },
        {
            "name": "Neven Munđar",
            "image": "images/team/neven.jpg",
            "twitter": "nmundar",
        },
        {
            "name": "Matija Marohnić",
            "image": "images/team/matija.jpg",
            "twitter": "silvenon",
        },
        {
            "name": "Krešimir Antolić",
            "image": "images/team/kreso.jpg",
            "twitter": "kantolic",
        },
    ]

    shuffle(team)
    shuffle(committee)

    return {
        "team": team,
        "committee": committee,
    }


def css_last_modified(request):
    css_last_modified = getmtime(abspath(join(dirname(__file__), 'dist/styles/style.css')))
    return {
        'css_last_modified': css_last_modified
    }
