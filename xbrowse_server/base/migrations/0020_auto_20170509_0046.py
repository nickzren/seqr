# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 00:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20170426_0348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='internal_case_review_brief_summary',
            new_name='internal_case_review_summary',
        ),
    ]
