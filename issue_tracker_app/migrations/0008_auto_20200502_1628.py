# Generated by Django 2.2.9 on 2020-05-02 16:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue_tracker_app', '0007_auto_20200127_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='ticket',
            name='upvotes',
            field=models.ManyToManyField(related_name='upvotes', through='issue_tracker_app.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
