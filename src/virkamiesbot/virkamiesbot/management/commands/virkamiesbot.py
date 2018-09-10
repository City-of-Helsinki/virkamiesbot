# -*- coding: utf-8 -*-

import logging
import pytz

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from virkamiesbot.bot import (fetch_decisions, simplify_decision_data,
    add_test_decision)
from virkamiesbot.twitter import handle_twitter, initialize_twitter
from virkamiesbot.models import Record

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Virkamiesbot runner management command'

    # This is the main method
    def handle(self, *args, **options):
        Record.objects.all().delete()
        latest_decision_time = init_latest_decision_time()
        decisions = fetch_decisions(since=latest_decision_time)
        decisions = simplify_decision_data(decisions)

        if len(decisions) == 0:
            decisions = add_test_decision()

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
        save_latest_decision(decisions, latest_decision_time)
        LOG.debug('Total: {0}'.format(len(decisions)))
        LOG.debug('Tweeted: {0}'.format(len(success_list)))
        LOG.debug('Failed to tweet: {0}'.format(len(fail_list)))

def save_latest_decision(decisions, previous_latest_time):
    latest_decision = get_latest_decision()
    latest = {'source_permalink': '', 'source_id': '',
              'source_created_at': previous_latest_time}
    for d in decisions:
        dt = datetime.strptime(d['last_modified_time'], "%Y-%m-%dT%H:%M:%S.%f")
        tz = pytz.timezone('Europe/Helsinki')
        dt = tz.localize(dt)
        if dt > latest['source_created_at']:
            latest = {'source_permalink': d['permalink'],
                      'source_id': d['id'],
                      'source_created_at':dt}
    if latest_decision:
        obj, created = Record.objects.update_or_create(pk=latest_decision.pk, defaults=latest)
        if created:
            return True
        else:
            LOG.info('Could not save time from previous decision to database')
            return False
    else:
        Record.objects.create(source_permalink=latest['source_permalink'],
                              source_created_at=latest['source_created_at'],
                              source_id=latest['source_id'])
    return True

def init_latest_decision_time():
    latest_decision = get_latest_decision()
    if not latest_decision:
        tz = pytz.timezone('Europe/Helsinki')
        date = datetime(2018, 9, 9, 1, 0)
        latest_decision_time = tz.localize(date)
    else:
        latest_decision_time = latest_decision.modified_at

    return latest_decision_time

def get_latest_decision():
    try:
        latest_decision = Record.objects.all().latest('modified_at')
    except ObjectDoesNotExist:
        return None

    return latest_decision

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2