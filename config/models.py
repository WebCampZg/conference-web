# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.deletion import PROTECT

from events.models import Event

from .singleton import SingletonModel


class SiteConfig(SingletonModel):
    """
    Holds global site configuration.
    """
    active_event = models.ForeignKey(Event, PROTECT, related_name='+')
    allow_talk_updates = models.BooleanField(
        help_text="If set to false, users will no longer be able to update talk descriptions.")
    community_vote_enabled = models.BooleanField(
        help_text="Enable the community vote page.")
