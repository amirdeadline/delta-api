from django.core.management.base import BaseCommand
from tenants_app.models import Customer, Tenant, Domain

class Command(BaseCommand):
    help = "Generate a reserved tenant"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            default="1000",
            type=str,
            help="Domain for the reserved tenant. "
            "Don't add your port or www here! on a local server you'll want to use localhost here (default)",
        )

    def handle(self, *args, **kwargs):
        # create your reserved tenant
        if Tenant.objects.filter(schema_name="reserved1000").first():
            self.stdout.write(self.style.ERROR('Tenant with schema_name reserved1000 already exists.'))
            return
        
        
        # get or create customer
        customer = Customer.objects.get(name= "DeltaSASE LLC").id
            # email='admin@deltasase.com',
            # defaults={
            #     'name': 'DeltaSASE LLC',
            #     'contact_number': '5134432021',
            #     'company_name': 'DeltaSASE LLC',
            #     'company_address': 'Test Address',
            # }
        # )

        tenant = Tenant(schema_name="reserved1000", name="Reserved 1000", customer_id=customer, detail={})
        tenant.save()

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = kwargs["domain"]
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()
