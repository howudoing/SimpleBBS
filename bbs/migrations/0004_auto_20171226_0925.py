# Generated by Django 2.0 on 2017-12-26 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0003_auto_20171226_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]