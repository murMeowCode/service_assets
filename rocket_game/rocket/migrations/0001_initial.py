# Generated by Django 5.2 on 2025-05-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveBigIntegerField()),
                ('spins_least', models.SmallIntegerField(default=3)),
                ('spin_cost', models.IntegerField(default=10)),
                ('spin_coef', models.FloatField(default=1)),
                ('life_upgrade_coef', models.FloatField(default=0)),
                ('oil_upgrade_coef', models.FloatField(default=0)),
                ('ammo_upgrade_coef', models.FloatField(default=0)),
            ],
        ),
    ]
