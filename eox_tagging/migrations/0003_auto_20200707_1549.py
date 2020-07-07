# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-07 15:49
from __future__ import unicode_literals

from django.db import migrations, models

import eox_tagging.constants


class Migration(migrations.Migration):

    dependencies = [
        ('eox_tagging', '0002_auto_20200630_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='invalidated_at',
            new_name='inactivated_at',
        ),
        migrations.AlterField(
            model_name='tag',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, b'INACTIVE'), (1, b'ACTIVE')], default=eox_tagging.constants.Status(1), editable=False),
        ),
    ]
