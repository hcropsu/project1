# Generated by Django 4.2.4 on 2023-08-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='berryentry',
            name='location',
            field=models.CharField(default='hillside', max_length=100),
            preserve_default=False,
        ),
    ]
