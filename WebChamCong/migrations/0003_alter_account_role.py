# Generated by Django 4.2.11 on 2024-05-18 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebChamCong', '0002_account_salary_alter_account_role_bangchamcong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(max_length=20),
        ),
    ]