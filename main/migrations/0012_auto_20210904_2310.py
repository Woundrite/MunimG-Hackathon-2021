# Generated by Django 3.2.7 on 2021-09-04 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210904_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='mics_expenses',
            new_name='misc_expenses',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_earning_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 4, 23, 10, 9, 933543)),
        ),
        migrations.AlterField(
            model_name='user',
            name='today',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 4, 23, 10, 9, 933543)),
        ),
    ]