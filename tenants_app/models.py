# Tenants_app models
from django.db import models ,transaction
from django_tenants.models import TenantMixin, DomainMixin
from django.core.exceptions import ValidationError  # Import ValidationError
from django.db.models import Max
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class ShareBase(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)
    detail = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        if not self.pk:  # Object is being created
            self.created_by = user_id
        self.modified_by = user_id
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        self.deleted_at = timezone.now()
        self.deleted_by = user_id
        super().delete(*args, **kwargs)

class ShareTag(models.Model):
    key = models.CharField(max_length=100)
    value = models.JSONField()
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class SDWANSoftware(ShareBase):
    tags = models.ManyToManyField(ShareTag, related_name='sdwan_software_tags', null=True, blank=True)
    production = models.BooleanField(default=True)
    url= models.URLField()

    def __str__(self):
        return f"{self.name} v{self.version}"

class Product(ShareBase):
    unit = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(ShareTag, related_name='products_tags', null=True, blank=True)
    
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
    tags = models.ManyToManyField(ShareTag, related_name='licenses', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Region(ShareBase):
    cloud = models.CharField(max_length=100)
    tags = models.ManyToManyField(ShareTag, related_name='regions', null=True, blank=True)
    
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
    tags = models.ManyToManyField(ShareTag, related_name='sces', null=True, blank=True)
    
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
    tags = models.ManyToManyField(ShareTag, related_name='sase_controllers', null=True, blank=True)
    
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
    tags = models.ManyToManyField(ShareTag, related_name='sdwan_controllers', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Contact(ShareBase):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(ShareTag, related_name='contacts_tags', null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'customer')

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(unique=True, max_length=200, db_index=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(ShareTag, related_name='customers_tags', null=True, blank=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    snapshot = models.TextField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    production = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    detail = models.JSONField(null=True, blank=True)
    admins = models.ManyToManyField('AdminUser', related_name='tenant_admins')
    products = models.ManyToManyField(Product, related_name='tenant_products')
    licenses = models.ManyToManyField(License, related_name='tenant_licenses')
    softwares = models.ManyToManyField(SDWANSoftware, related_name='tenant_softwares')
    tags = models.ManyToManyField(ShareTag, related_name='tenants_tags', null=True, blank=True)
    config = models.URLField(blank=True)
    auto_drop_schema = True

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
    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.children.exists():
            logger.error("Attempt to delete tenant with existing children")
            raise Exception("Cannot delete tenant because it has child tenants.")
        if self.enabled:
            logger.error("Attempt to delete tenant that is enabled")
            raise Exception("Cannot delete tenant because it is currently enabled.")
        super(Tenant, self).delete(*args, **kwargs)

class Domain(DomainMixin):
    pass

class IKEEncryption(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class IKEHash(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class IKEDHGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class IKERPF(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ESPEncryption(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ESPHash(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ESPDHGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ESPPFS(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RoutingProtocol(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class InterfaceType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class InterfaceRole(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class VRFRole(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class LACPHashOption(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class DeviceModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class DeletedTenant(models.Model):
    tenant_id = models.IntegerField(db_index=True)
    schema_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)
    snapshot = models.TextField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    config = models.URLField(blank=True)
    detail = models.JSONField(null=True, blank=True)
    

    def __str__(self):
        return self.schema_name