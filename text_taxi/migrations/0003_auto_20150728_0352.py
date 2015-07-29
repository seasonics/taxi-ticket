# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('text_taxi', '0002_auto_20150715_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxi',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 3, 51, 59, 794397, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 3, 52, 16, 918555, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(default='cool', max_length=256),
            preserve_default=False,
        ),
    ]
