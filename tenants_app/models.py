# Tenants_app models
from django.db import models ,transaction
from django_tenants.models import TenantMixin, DomainMixin
from django.core.exceptions import ValidationError  # Import ValidationError
from django.db.models import Max
import logging

logger = logging.getLogger(__name__)


class ShareBase(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100)
    detail = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Tag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = JSONField()
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class Product(ShareBase):
    unit = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='products_tags')
    
    def __str__(self):
        return self.name

class ProductCategory(ShareBase):
    unit = models.CharField(max_length=100)
    ppu = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class License(ShareBase):
    unit = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(Tag, related_name='licenses')
    
    def __str__(self):
        return self.name

class Region(ShareBase):
    cloud = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='regions')
    
    def __str__(self):
        return self.name

class SCE(ShareBase):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    total_capacity = models.IntegerField()
    available_capacity = models.IntegerField()
    mgmt_ip = models.GenericIPAddressField()
    mgmt_url = models.URLField()
    certificate = models.TextField()
    enabled = models.BooleanField(default=True)
    dedicated = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='sces')
    
    def __str__(self):
        return self.name

class SASEController(ShareBase):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    mgmt_ip = models.GenericIPAddressField()
    mgmt_url = models.URLField()
    pub_ip = models.GenericIPAddressField()
    pub_url = models.URLField()
    certificate = models.TextField()
    enabled = models.BooleanField(default=True)
    dedicated = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='sase_controllers')
    
    def __str__(self):
        return self.name

class SDWANController(ShareBase):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    mgmt_ip = models.GenericIPAddressField()
    mgmt_url = models.URLField()
    pub_ip = models.GenericIPAddressField()
    pub_url = models.URLField()
    certificate = models.TextField()
    enabled = models.BooleanField(default=True)
    dedicated = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='sdwan_controllers')
    
    def __str__(self):
        return self.name

class Contact(ShareBase):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='contacts_tags')
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(unique=True, max_length=200, db_index=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    contacts = models.ManyToManyField(Contact, related_name='customers_contacts')
    tags = models.ManyToManyField(Tag, related_name='customers_tags')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class AdminUser(ShareBase):
    username = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255)  # Keycloak UUID for the user


class Tenant(TenantMixin):
    tenant_id = models.IntegerField(unique=True, db_index=True)
    schema_name = models.CharField(max_length=255, unique=True)
    name = models.CharField(unique=True, max_length=255, db_index=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    snapshot = models.TextField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    production = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    detail = JSONField()
    admins = models.ManyToManyField('AdminUser', related_name='tenant_admins')
    products = models.ManyToManyField(Product, related_name='tenant_products')
    licenses = models.ManyToManyField(License, related_name='tenant_licenses')


    def __str__(self):
        return self.schema_name

    def get_children(self):
        return self.children.all()

    @transaction.atomic
    def save(self, *args, **kwargs):
        try:
            if self.schema_name == "public":
                logger.debug("Setting schema name to 'public'")
                self.tenant_id = 1
                self.schema_name = 'public'
            elif self.schema_name == "reserved1000":
                logger.debug("Setting schema name to 'reserved1000'")
                self.tenant_id = 1000
                self.schema_name = 'reserved1000'
            else:
                if self.pk is None:  # This is a new record
                    max_id = Tenant.objects.all().aggregate(Max('tenant_id'))['tenant_id__max']
                    if max_id is None:  # This is the first record
                        self.tenant_id = 1
                    else:
                        self.tenant_id = max_id + 1
                    self.schema_name = 'Tenant_' + str(self.tenant_id)

            super(Tenant, self).save(*args, **kwargs)
        except Exception as e:
            logger.error("Error saving tenant: %s", e)
            raise


class Domain(DomainMixin):
    pass


class IKEEncryption(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IKEHash(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IKEDHGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IKERPF(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ESPEncryption(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ESPHash(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ESPDHGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ESPPFS(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RoutingProtocol(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
