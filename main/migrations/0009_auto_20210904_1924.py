# Generated by Django 3.2.7 on 2021-09-04 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210904_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10000)),
                ('surname', models.CharField(max_length=10000)),
                ('expenses', models.CharField(default='0', max_length=100000)),
                ('savings', models.CharField(default='', max_length=100000)),
                ('monthly_earnings', models.CharField(default='', max_length=100000)),
                ('last_earning_add', models.DateTimeField(default=datetime.datetime(2021, 9, 4, 19, 24, 52, 890858))),
                ('today', models.DateTimeField(default=datetime.datetime(2021, 9, 4, 19, 24, 52, 890858))),
                ('email', models.EmailField(max_length=10000)),
                ('password', models.CharField(max_length=1000)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]