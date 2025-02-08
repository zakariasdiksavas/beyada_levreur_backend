# Generated by Django 5.1.5 on 2025-01-27 14:04

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('production', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('poids_plateau', models.FloatField(default=0)),
                ('pu', models.FloatField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('is_delivered', models.BooleanField(default=False)),
                ('auto_created', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now=True)),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='commands', to='base.batiment')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='commands', to='base.client')),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='commands', to=settings.AUTH_USER_MODEL)),
                ('production_source', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='production.production')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCommande',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('poids_plateau', models.FloatField(default=0)),
                ('pu', models.FloatField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('is_delivered', models.BooleanField(default=False)),
                ('auto_created', models.BooleanField(default=False)),
                ('created_at', models.DateField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('batiment', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base.batiment')),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base.client')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('production_source', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='production.production')),
            ],
            options={
                'verbose_name': 'historical commande',
                'verbose_name_plural': 'historical commandes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
