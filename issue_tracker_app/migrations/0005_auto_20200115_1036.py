# Generated by Django 2.2.9 on 2020-01-15 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker_app', '0004_auto_20200114_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_text',
        ),
    ]
