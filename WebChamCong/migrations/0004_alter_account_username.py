# Generated by Django 4.2.13 on 2024-05-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebChamCong', '0003_alter_account_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]