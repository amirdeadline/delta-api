# Generated by Django 5.0.6 on 2024-05-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.JSONField(blank=True, default=dict, null=True)),
                ('object_id', models.BigIntegerField(editable=False)),
            ],
            options={
                'indexes': [models.Index(fields=['object_id'], name='base_tag_object__d024f1_idx'), models.Index(fields=['key', 'object_id'], name='base_tag_key_fd57b8_idx')],
                'unique_together': {('key', 'object_id')},
            },
        ),
    ]
