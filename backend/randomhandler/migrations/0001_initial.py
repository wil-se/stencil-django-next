# Generated by Django 4.2 on 2023-04-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashChainIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chain', models.CharField(default='zero', unique=True)),
                ('index', models.PositiveBigIntegerField(default=0, editable=False)),
            ],
        ),
    ]
