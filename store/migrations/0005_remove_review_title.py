# Generated by Django 4.1.7 on 2023-05-12 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
    ]
