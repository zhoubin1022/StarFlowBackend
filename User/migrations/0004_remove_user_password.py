# Generated by Django 3.2.9 on 2021-11-17 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20211111_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]