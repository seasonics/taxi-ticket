# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_taxi', '0004_auto_20150729_0046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='taxies',
            new_name='taxis',
        ),
    ]
