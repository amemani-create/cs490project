# Generated by Django 3.1 on 2021-03-05 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_snippet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='snippet',
        ),
    ]
