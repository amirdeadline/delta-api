# Generated by Django 5.0.6 on 2024-05-21 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('fqdn', models.CharField(max_length=255)),
                ('tls_enabled', models.BooleanField(default=False)),
                ('tls_certificate', models.CharField(blank=True, max_length=100, null=True)),
                ('tls_key', models.CharField(blank=True, max_length=100, null=True)),
                ('ca_certificate', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CACertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('certificate_type', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('certificate_url', models.URLField()),
                ('private_key_url', models.URLField()),
                ('issuer', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('ca_bundle_url', models.URLField(blank=True, null=True)),
                ('is_root_ca', models.BooleanField(default=False)),
                ('type', models.CharField(default='ca', editable=False, max_length=20)),
                ('signing_policies', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('certificate_type', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('certificate_url', models.URLField()),
                ('private_key_url', models.URLField()),
                ('custom_field', models.CharField(max_length=255)),
                ('custom_data', models.JSONField()),
                ('type', models.CharField(default='custom', editable=False, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DSNDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('vendor', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('software', models.CharField(max_length=255, verbose_name='Software Version')),
                ('serial_number', models.CharField(max_length=255)),
                ('certificate', models.URLField()),
                ('trusted_ca', models.URLField()),
                ('descriptions', models.TextField(blank=True, null=True)),
                ('registered', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MachineGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('compliance', models.CharField(max_length=255, verbose_name='Compliance Standard')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SSHCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('certificate_type', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('certificate_url', models.URLField()),
                ('private_key_url', models.URLField()),
                ('authorized_keys', models.TextField()),
                ('type', models.CharField(default='ssh', editable=False, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SSLCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('certificate_type', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('certificate_url', models.URLField()),
                ('private_key_url', models.URLField()),
                ('issuer', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('ca_bundle_url', models.URLField(blank=True, null=True)),
                ('type', models.CharField(default='ssl', editable=False, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VRF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActiveDirectoryServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('domain', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='AzureADServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('tenant_id', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('redirect_uri', models.URLField(blank=True, max_length=1024, null=True)),
                ('domain', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='CustomServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('type', models.CharField(default='custom', editable=False, max_length=50)),
                ('custom_data', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='DNSServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('dnssec_active', models.BooleanField(default=False)),
                ('unsigned_check', models.BooleanField(default=False)),
                ('timecheck', models.BooleanField(default=False)),
                ('dnssec_class', models.CharField(blank=True, max_length=50, null=True)),
                ('key_tag', models.CharField(blank=True, max_length=50, null=True)),
                ('algorithm', models.CharField(blank=True, max_length=50, null=True)),
                ('digest_type', models.CharField(blank=True, max_length=10, null=True)),
                ('digest', models.CharField(blank=True, max_length=255, null=True)),
                ('public_key', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='FileServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('storage_capacity', models.CharField(max_length=255)),
                ('protocol', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='IdPServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('entity_id', models.CharField(max_length=255)),
                ('sso_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('slo_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('public_cert', models.TextField(blank=True, null=True)),
                ('private_key', models.TextField(blank=True, null=True)),
                ('metadata_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('api_key', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='IPFixCollector',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('protocol', models.IntegerField()),
                ('port', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='LDAPServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('base_dn', models.CharField(max_length=255)),
                ('port', models.IntegerField(default=389)),
                ('use_ssl', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='NTPServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('version', models.IntegerField()),
                ('auth_key', models.CharField(blank=True, max_length=100, null=True)),
                ('max_poll', models.IntegerField()),
                ('min_poll', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='RADIUSServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('secret', models.CharField(max_length=255)),
                ('auth_port', models.IntegerField(default=1812)),
                ('acct_port', models.IntegerField(default=1813)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='SyslogServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('port', models.IntegerField()),
                ('transport_protocol', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='WebServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resources_app.server')),
                ('technology', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources_app.server',),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('detail', models.JSONField()),
                ('type', models.CharField(choices=[('laptop', 'Laptop'), ('phone', 'Phone'), ('tablet', 'Tablet'), ('network', 'Network Device'), ('other', 'Other')], max_length=50)),
                ('vendor', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('os', models.CharField(choices=[('windows', 'Windows'), ('linux', 'Linux'), ('mac_os', 'Mac OS'), ('ios', 'iOS'), ('android', 'Android')], max_length=50)),
                ('serial_number', models.CharField(max_length=255)),
                ('certificate', models.URLField()),
                ('trusted_ca', models.URLField()),
                ('admins', models.JSONField()),
                ('users', models.JSONField()),
                ('device_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices_device_group', to='resources_app.machinegroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
