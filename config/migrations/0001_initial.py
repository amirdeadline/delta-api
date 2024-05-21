# Generated by Django 5.0.6 on 2024-05-21 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SnapshotConfig',
            fields=[
                ('configbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='config.configbase')),
                ('url', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('config.configbase',),
        ),
        migrations.CreateModel(
            name='CandidateConfig',
            fields=[
                ('configbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='config.configbase')),
                ('committed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('committed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('committed', models.BooleanField(default=False)),
                ('changes', models.JSONField(default=dict)),
                ('base_snapshot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='base_snapshots', to='config.snapshotconfig')),
            ],
            options={
                'abstract': False,
            },
            bases=('config.configbase',),
        ),
    ]
