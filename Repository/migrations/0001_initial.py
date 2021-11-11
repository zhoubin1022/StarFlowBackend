# Generated by Django 3.2.9 on 2021-11-11 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('repo_name', models.CharField(max_length=30)),
                ('finished', models.IntegerField(default=0)),
                ('checking', models.IntegerField(default=0)),
                ('incomplete', models.IntegerField(default=0)),
                ('repo_member', models.IntegerField(default=1)),
            ],
        ),
    ]