# Tenants_app models
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.core.exceptions import ValidationError  # Import ValidationError
from django.db.models import Max


class Customer(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(max_length=200, unique=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

def validate_schema_name(value):
    if value != "default":
        try:
            int(value)
        except ValueError:
            raise ValidationError(
                f'{value} is not an integer or "default"'
            )


class Tenant(TenantMixin):
    tenant_id = models.IntegerField(unique=True, db_index=True) 
    schema_name = models.CharField(max_length=255, unique=True, validators=[validate_schema_name])
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    snapshot = models.TextField(max_length=200, null=True, blank=True)
    customer_id= models.ForeignKey(Customer, on_delete=models.PROTECT)
    enabled = models.BooleanField(default=True)
    production = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.schema_name

    def get_children(self):
        return self.children.all()

    def save(self, *args, **kwargs):
        if self.schema_name=="public":
            print(50*"#",self.schema_name)
            self.tenant_id = 1
            self.schema_name = 'public'

        elif self.schema_name=="reserved1000":
            print(50*"#",self.schema_name)
            self.tenant_id = 1000
            self.schema_name = 'reserved1000'

        else:
            print(50*"$", "problem",self.schema_name)

            if self.pk is None:  # This is a new record
                max_id = Tenant.objects.all().aggregate(Max('tenant_id'))['tenant_id__max']
                if max_id is None:  # This is the first record
                    self.tenant_id = 1
                else:
                    self.tenant_id = max_id + 1

            self.schema_name = 'Tenant_' + str(self.tenant_id)
            

        super(Tenant, self).save(*args, **kwargs)



class Domain(DomainMixin):
    pass
