# Generated by Django 5.1.5 on 2025-02-01 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charge', '0003_charge_classe_historicalcharge_classe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charge',
            old_name='commade',
            new_name='commande',
        ),
        migrations.RenameField(
            model_name='historicalcharge',
            old_name='commade',
            new_name='commande',
        ),
    ]
