# Generated by Django 2.0 on 2017-12-26 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0005_userprofile_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='friends',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='_userprofile_friends_+', to='bbs.UserProfile'),
        ),
    ]
