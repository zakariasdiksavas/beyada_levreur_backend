# Generated by Django 5.1.5 on 2025-02-03 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('classe', models.IntegerField(choices=[(1, 'normal'), (2, 'double jaune'), (3, 'blanc'), (4, 'sale'), (5, 'casse'), (6, 'elimine'), (7, 'triage')], default=1)),
                ('is_plus', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventaire_batiment', to='base.batiment')),
            ],
        ),
    ]
