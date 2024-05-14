# Generated by Django 5.0.5 on 2024-05-14 17:58

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebChamCong', '0002_customuser_delete_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Timekeeping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
                ('hourly_rate', models.FloatField()),
                ('total_salary', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]