# Generated by Django 4.2.3 on 2023-07-17 07:34

from django.db import migrations, models
import django.db.models.deletion
import tenants_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_address', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.IntegerField(db_index=True, unique=True)),
                ('schema_name', models.CharField(max_length=255, unique=True, validators=[tenants_app.models.validate_schema_name])),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('snapshot', models.TextField(blank=True, max_length=200, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('production', models.BooleanField(default=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenants_app.customer')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='tenants_app.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='tenants_app.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
