# Generated by Django 4.2 on 2023-04-26 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomhandler', '0008_alter_hashchainindex_chain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractednumber',
            name='chain',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='extractednumber',
            name='signed_private_seed_base64',
            field=models.CharField(max_length=400),
        ),
    ]
