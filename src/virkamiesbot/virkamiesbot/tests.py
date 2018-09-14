# -*- coding: utf-8 -*-
import json
import mock
import pytz
import tweepy

from datetime import datetime
from django.test import TestCase
from django.core.management.base import BaseCommand
from django.utils import timezone
from virkamiesbot.management.commands.virkamiesbot import Command
from virkamiesbot.models import Record

from virkamiesbot.bot import (get_policymaker_ids, simplify_decision_data,
    fetch_decisions, districts_to_string, add_test_decision)

from virkamiesbot.twitter import (handle_twitter, tweet, generate_tweet_text,
    tags_to_string, shorten_message)

TZ = pytz.timezone('Europe/Helsinki')

class CommandTestCase(TestCase):
    virkamiesbot_cmd = Command()
    decisions = None
    time_string = ''
    time = None

    def setUp(self):
        self.set_time_string('2015-05-10T19:43:19.620505')
        Record.objects.create(source_created_at=self.time,
                              source_permalink='http://www.google.fi',
                              source_id='1234567890abcdefghijklmnopqrs')
        self.decisions = self.get_simplified_test_decision()
        self.set_time_string('2015-05-10T19:43:19.620505')

    def get_simplified_test_decision(self):
        decision = [{
                "policymaker": "Kopiovastaava",
                "content": "Kopiovastaava muuttaa Amerikkaan 20.9.2018. Heidän korkeutensa ostaa golf-välineet ja harppuunan. Varokoot krokotiilit golf-kentällä.",
                "districts": "Kiikka,Tormilankylä",
                "permalink": "http://www.google.fi",
                "id": "12345789",
                "last_modified_time": "2018-03-25T11:09:06.806929"},
            ]
        return decision

    def set_time(self):
        self.time = datetime.strptime(self.time_string, "%Y-%m-%dT%H:%M:%S.%f")
        self.time = TZ.localize(self.time)

    def set_time_string(self, t_str):
        self.time_string = t_str
        self.set_time()

    def test_save_latest_decision(self):
        self.update_time_string()
        self.assertEqual(self.virkamiesbot_cmd.save_latest_decision(self.decisions, self.time), True)

    def test_time_string_to_datetime(self):
        self.assertEqual(self.virkamiesbot_cmd.time_string_to_datetime(self.time_string), self.time)

    def update_time_string(self):
        self.time_string = '2018-09-10T8:15:13.123456'

class BotTestCase(TestCase):
    decisions = None

    def create_test_decisions(*args, **kwargs):
        decision = None
        with open('src/virkamiesbot/virkamiesbot/test_utilities/test_decision.txt') as file:
            decision = json.loads(file.read())
        return decision

    @mock.patch('virkamiesbot.bot.get_policymaker_ids', return_value=["u5110510010vh1","u511051002020vh1"])
    @mock.patch('virkamiesbot.bot.query_open_ahjo', side_effect=create_test_decisions)
    def test_fetch_decisions(self, mock_get_policymaker_ids, mock_query_open_aohjo):
        self.assertNotEqual(fetch_decisions(), [])


class TwitterTestCase(TestCase):
    decision_data = {}

    def setUp(self):
        self.set_decision_data()
    
    def set_decision_data(self):
        time = timezone.now()
        self.decision_data = {"policymaker": "Kopiovastaava",
                         "content": "Kopiovastaava muuttaa Amerikkaan 20.9.2018. Heidän korkeutensa ostaa golf-välineet ja harppuunan. Varokoot krokotiilit golf-kentällä.",
                         "districts": "Kiikka,Tormilankylä",
                         "permalink": "http://www.google.fi",
                         "id": "12345789",
                         "last_modified_time": time}

    def test_generate_tweet_text(self):
        self.assertLess(len(generate_tweet_text(self.decision_data)), 240)





# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2