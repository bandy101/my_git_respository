# Generated by Django 2.1.7 on 2019-04-06 12:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190406_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 6, 12, 29, 50, 646251, tzinfo=utc)),
        ),
    ]