from django.core.management.base import BaseCommand
from tenants_app.models import Customer, Tenant, Domain

class Command(BaseCommand):
    help = "Generate the public tenant"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            default="localhost",
            type=str,
            help="Domain for the public domain. "
            "Don't add your port or www here! on a local server you'll want to use localhost here (default)",
        )

    def handle(self, *args, **kwargs):
        # create your public tenant
        if Tenant.objects.filter(schema_name="public").first():
            return
        
        # get or create customer
        customer, created = Customer.objects.get_or_create(
            email='admin@deltasase.com',
            defaults={
                'name': 'DeltaSASE LLC',
                'contact_number': '5134432021',
                'company_name': 'DeltaSASE LLC',
                'company_address': 'Test Address',
            }
        )

        tenant = Tenant(schema_name="public", name="Schemas Inc.", customer_id=customer)
        tenant.save()

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = kwargs["domain"]
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

