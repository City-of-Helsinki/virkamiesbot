# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from virkamiesbot.bot import fetch_decisions
from virkamiesbot.twitter import handle_twitter, initialize_twitter

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Virkamiesbot runner management command'

    # This is the main method
    def handle(self, *args, **options):
        decisions = fetch_decisions()
        twitter = initialize_twitter()
        success_list = []
        for d in decisions:
            tweet_successful = handle_twitter(d, twitter)
            if tweet_successful:
                success_list.append(d)
            else:
                success_list.append('------------failed------------')
        print(success_list)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
