# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0001_initial'),
        ('twitter', '0002_auto_20150506_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.CharField(max_length=140)),
                ('tweet_id', models.BigIntegerField()),
                ('favorites', models.IntegerField()),
                ('tweet_date', models.DateTimeField()),
                ('keyword', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='sentiment',
            name='company',
        ),
        migrations.DeleteModel(
            name='Sentiment',
        ),
        migrations.AddField(
            model_name='tweet',
            name='sentiment',
            field=models.ForeignKey(to='sentiment.Sentiment'),
        ),
    ]
