# -*- coding: utf-8 -*-

import logging

from django.db import models

LOG = logging.getLogger(__name__)


class Record(models.Model):
    source_created_at = models.DateTimeField()
    source_permalink = models.CharField(max_length=2048)
    source_id = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
