# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
