# Generated by Django 2.1.5 on 2023-02-09 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_page_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='likes',
        ),
    ]