from django.core.management.base import BaseCommand
from tenants_app.models import Tenant, Domain, Customer, Contact

class Command(BaseCommand):
    help = "Generate the public tenant"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            default="localhost",
            type=str,
            help="Domain for the public domain. Don't add your port or www here! On a local server, you'll want to use localhost here (default)."
        )
        parser.add_argument(
            "--enabled",
            action='store_true',
            help="Flag to specify if the tenant should be enabled. Defaults to True.",
            default=True
        )
        parser.add_argument(
            "--production",
            action='store_true',
            help="Flag to specify if the tenant should be marked as production. Defaults to True.",
            default=True
        )

    def handle(self, *args, **options):
        # Check if the public tenant already exists
        if Tenant.objects.filter(schema_name="public").exists():
            self.stdout.write(self.style.WARNING('Public tenant already exists'))
            return
        
        # Create contact
        # contact = Contact.objects.create(
        #     name='Admin Contact',
        #     email='admin@deltasase.com',  # Assuming email is a field in Contact model
        #     number='5134432021',  # Assuming number is a field in Contact model
        #     address='Test Address',  # Assuming address is a field in Contact model
        #     detail={} 
        # )

        # Create customer and link the contact
        customer = Customer.objects.create(
            name='DeltaSASE LLC',
            company_name='DeltaSASE LLC',
            is_active=True,
        )
        # customer.contacts.add(contact)
        
        # Create the public tenant with the created customer
        tenant = Tenant.objects.create(
            schema_name="public",
            name="Delta SASE",
            customer=customer,
            description="Public tenant for Delta SASE company itself",
            enabled=options['enabled'],
            production=options['production'],
            detail={} 
        )

        # Add one or more domains for the tenant
        domain = Domain.objects.create(
            domain=options["domain"],
            tenant=tenant,
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully created public tenant with domain: {}'.format(options["domain"])))
        self.stdout.write(self.style.SUCCESS('Tenant Enabled: {}'.format(options["enabled"])))
        self.stdout.write(self.style.SUCCESS('Tenant Production: {}'.format(options["production"])))
