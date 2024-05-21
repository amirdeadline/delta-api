import psycopg2
from psycopg2 import sql
from django.conf import settings
from django_tenants.signals import schema_migrated, schema_migrate_message#, run_migrations
from django.dispatch import receiver
from django_tenants.models import TenantMixin, DomainMixin

import logging


logger = logging.getLogger(__name__)

def create_initial_tenant_setting(schema_name):
    # Get database settings from Django settings
    db_settings = settings.DATABASES['default']

    try:
        # Connect to your PostgreSQL database using settings from settings.py
        connection = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT'],
        )
        cursor = connection.cursor()

        # Set the search_path to the tenant's schema
        cursor.execute(sql.SQL('SET search_path TO {};').format(sql.Identifier(schema_name)))

        # Create the initial TenantSetting entry with ID 1
        insert_query = sql.SQL(f"""
            INSERT INTO {schema_name}.settings_app_tenantsetting (id, description, sase_bgp_asn, sdwan_bgp_asn, sase_community, sdwan_community, unique_constraint)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (unique_constraint) DO NOTHING;
        """)

        cursor.execute(insert_query, (1, '', 64512, 64513, '64512:1', '64513:1', 1))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        logger.info("Initial TenantSetting created successfully.")
    
    except Exception as error:
        logger.error(f"Error creating initial TenantSetting: {error}")

# def create_initial_tenant_setting(schema_name):
#     # Get database settings from Django settings
#     db_settings = settings.DATABASES['default']

#     try:
#         # Connect to your PostgreSQL database using settings from settings.py
#         connection = psycopg2.connect(
#             dbname=db_settings['NAME'],
#             user=db_settings['USER'],
#             password=db_settings['PASSWORD'],
#             host=db_settings['HOST'],
#             port=db_settings['PORT'],
#         )
#         cursor = connection.cursor()

#         # Set the search_path to the tenant's schema
#         cursor.execute(sql.SQL('SET search_path TO {};').format(sql.Identifier(schema_name)))

#         # Query the list of all tables in the specified schema
#         cursor.execute(sql.SQL("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = %s;
#         """), [schema_name])

#         # Fetch all table names and log them
#         tables = cursor.fetchall()
#         logger.info(f"Tables in schema '{schema_name}': {tables}")

#         # Close the cursor and connection
#         cursor.close()
#         connection.close()

#     except Exception as error:
#         logger.error(f"Error querying tables in schema '{schema_name}': {error}")


@receiver(schema_migrated, sender=TenantMixin)
def handle_schema_migrated(sender, **kwargs):
    schema_name = kwargs['schema_name']
    print(schema_name, "created!!!!!!!!!")

    if schema_name[0:7]=="tenant_":
        create_initial_tenant_setting(schema_name)

    # recreate materialized views in the schema



# post_schema_sync





# # Receiver to handle schema_migrated signal
# @receiver(schema_migrate_message)
# def handle_schema_migrated(sender, **kwargs):
#     schema_name = kwargs['schema_name']
#     # Print schema name in red color for troubleshooting
#     print(f"\033[91mSchema name: {schema_name}\033[0m")
#     create_initial_tenant_setting(schema_name)
#     logger.info(f"Schema migrated and initial TenantSetting created for {schema_name}")
