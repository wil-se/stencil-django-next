# Generated by Django 4.2 on 2023-04-25 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instantgame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instantgame',
            name='bet_amount',
            field=models.FloatField(default=1),
        ),
    ]
