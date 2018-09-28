# -*- coding: utf-8 -*-
import logging
import pytz

from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from virkamiesbot.bot import (fetch_decisions, simplify_decision_data)
from virkamiesbot.twitter import handle_twitter, initialize_twitter
from virkamiesbot.models import Record

LOG = logging.getLogger(__name__)

TZ = pytz.timezone('Europe/Helsinki')
DESTROY_RECORDS_AFTER = timedelta(hours=1)

class Command(BaseCommand):
    help = 'Virkamiesbot runner management command'

    # This is the main method
    def handle(self, *args, **options):
        latest_decision_time = self.init_latest_decision_time()
        policymaker_decisions = fetch_decisions(since=latest_decision_time)
        decisions = simplify_decision_data(policymaker_decisions)
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
        self.remove_old_records()

    def save_latest_decision(self, decisions, previous_latest_time):
        # decisions must be a list
        # previous_latest_time has to be timezone aware datetime object

        latest = {'permalink': '',
                  'id': '',
                  'created_at':''}

        for d in decisions:
            dt = self.time_string_to_datetime(d['last_modified_time'])
            if dt > previous_latest_time:
                latest = {'permalink': d['permalink'],
                        'id': d['id'],
                        'created_at':dt}

        if latest['id'] != '':
            try:
                Record.objects.create(source_permalink=latest['permalink'],
                                      source_id=latest['id'],
                                      source_created_at=latest['created_at'])
            except IntegrityError as e:
                LOG.error(e)
                return False
            return True
        return False

    def init_latest_decision_time(self):
        latest_decision = self.get_latest_decision()
        if not latest_decision:
            tz = pytz.timezone('Europe/Helsinki')
            date = datetime(2018, 9, 10, 1, 0)
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

    def remove_old_records(self):
        delete_before_date = timezone.now() - DESTROY_RECORDS_AFTER
        Record.objects.all().filter(modified_at__lt=delete_before_date).delete()
        return

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2