# Generated by Django 4.2 on 2023-04-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomhandler', '0005_alter_extractednumber_chain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractednumber',
            name='chain',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='extractednumber',
            name='number',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='extractednumber',
            name='signed_private_seed_base64',
            field=models.CharField(max_length=512),
        ),
    ]
