# Generated by Django 2.2 on 2021-08-30 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msifilters',
            name='filter_name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
