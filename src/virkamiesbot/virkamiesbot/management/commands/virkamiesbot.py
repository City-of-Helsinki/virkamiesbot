# -*- coding: utf-8 -*-

import logging
import pytz

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from virkamiesbot.bot import (fetch_decisions, simplify_decision_data)
from virkamiesbot.twitter import handle_twitter, initialize_twitter
from virkamiesbot.models import Record

LOG = logging.getLogger(__name__)

TZ = pytz.timezone('Europe/Helsinki')


class Command(BaseCommand):
    help = 'Virkamiesbot runner management command'

    # This is the main method
    def handle(self, *args, **options):
        latest_decision_time = self.init_latest_decision_time()
        decisions = fetch_decisions(since=latest_decision_time)
        decisions = simplify_decision_data(decisions)
        twitter = initialize_twitter()
        success_list = []
        fail_list = []
        for idx, d in enumerate(decisions):
            tweet_successful = handle_twitter(d, twitter)
            if tweet_successful:
                # LOG.info("{0} tweeted ({1})".format((idx+1), 
                                                        # d['policymaker']))
                success_list.append('Policymaker: {0}, time: {1}'.format(d['policymaker'], d['last_modified_time']))
            else:
                # LOG.info("{0} failed ({1})".format((idx+1), d['policymaker']))
                fail_list.append('Policymaker:{0}, {1}'.format(d['policymaker'], d['last_modified_time']))
        self.save_latest_decision(decisions, latest_decision_time)
        LOG.debug('Total: {0}'.format(len(decisions)))
        LOG.debug('Tweeted: {0}'.format(len(success_list)))
        LOG.debug('Failed to tweet: {0}'.format(len(fail_list)))


    def save_latest_decision(self, decisions, previous_latest_time):
        # decisions must be a list
        # previous_latest_time has to be timezone aware datetime object

        latest = {'source_permalink': '',
                  'source_id': '',
                  'source_created_at':''}

        for d in decisions:
            dt = self.time_string_to_datetime(d['last_modified_time'])
            if dt > previous_latest_time:
                latest = {'source_permalink': d['permalink'],
                        'source_id': d['id'],
                        'source_created_at':dt}

        if latest['source_id'] == '':
            try:
                obj, created = Record.objects.update_or_create(id=1, defaults=latest)
            except IntegrityError as e:
                LOG.error(e)
                return False

            if created:
                LOG.info("Created new Record")
            else:
                LOG.info("Updated Record")
            return True

        return False

    def init_latest_decision_time(self):
        latest_decision = self.get_latest_decision()
        if not latest_decision:
            tz = pytz.timezone('Europe/Helsinki')
            date = datetime(2018, 9, 13, 1, 0)
            latest_decision_time = tz.localize(date)
        else:
            latest_decision_time = latest_decision.modified_at

        return latest_decision_time

    def get_latest_decision(self):
        try:
            latest_decision = Record.objects.all().latest('modified_at')
        except ObjectDoesNotExist:
            return None

        return latest_decision
    
    def time_string_to_datetime(self, time_string):
        dt = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
        dt = TZ.localize(dt)
        return dt

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2