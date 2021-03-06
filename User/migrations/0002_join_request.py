# Generated by Django 3.2.9 on 2021-11-11 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Repository', '0002_member'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.IntegerField(default=-1)),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Repository.repository')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
    ]
