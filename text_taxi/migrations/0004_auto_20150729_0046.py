# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_taxi', '0003_auto_20150728_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.CharField(unique=True, max_length=24),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
