# Generated by Django 3.0 on 2021-03-18 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_booksmodel_books_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksmodel',
            name='books_data',
        ),
        migrations.RemoveField(
            model_name='booksmodel',
            name='url',
        ),
        migrations.RemoveField(
            model_name='booksmodel',
            name='user',
        ),
        migrations.CreateModel(
            name='BooksUrlModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, null=True)),
                ('books_data', models.CharField(max_length=5000, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
