# Generated by Django 3.0 on 2021-03-18 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210318_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksmodel',
            name='average_rating',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='booksmodel',
            name='ratings_count',
            field=models.IntegerField(null=True),
        ),
    ]
