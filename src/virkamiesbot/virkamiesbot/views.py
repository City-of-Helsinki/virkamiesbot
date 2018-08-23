# -*- coding: utf-8 -*-

import logging
import pprint
from django.shortcuts import render
from django.views.generic import View
from virkamiesbot.bot import fetch_decisions

pp = pprint.PrettyPrinter(indent=4)

LOG = logging.getLogger(__name__)

class Index(View):
    d = fetch_decisions()
    pp.pprint("##########################")
    pp.pprint(d.text)
