# Generated by Django 5.1.5 on 2025-01-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiements', '0002_alter_paiementtry_paiement_by_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpaiementtry',
            name='status',
            field=models.IntegerField(choices=[(1, 'en cours'), (2, 'payé'), (3, 'échec')], default=1),
        ),
        migrations.AddField(
            model_name='paiementtry',
            name='status',
            field=models.IntegerField(choices=[(1, 'en cours'), (2, 'payé'), (3, 'échec')], default=1),
        ),
    ]
