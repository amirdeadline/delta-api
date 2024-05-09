# reserces_app/models.py
from django.db import models
from django.db.models import JSONField
# from django.contrib.postgres.fields import JSONField
from polymorphic.models import PolymorphicModel
import logging
from base.models import BaseModel, BasePolymorphic

logger = logging.getLogger(__name__)
        
class ResourceBase(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    detail = JSONField()

    class Meta:
        abstract = True

class Certificate(ResourceBase):
    certificate_type = models.CharField(max_length=100)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    certificate_url = models.URLField()
    private_key_url = models.URLField()  # URL to the vault location

    class Meta:
        abstract = True

class CACertificate(Certificate):
    issuer = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    ca_bundle_url = models.URLField(blank=True, null=True)  # Optional CA bundle URL
    is_root_ca = models.BooleanField(default=False)  # Flag to identify if this is a Root CA
    type = models.CharField(max_length=20, default='ca', editable=False)
    signing_policies = models.TextField() 

class SSLCertificate(Certificate):
    issuer = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    ca_bundle_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, default='ssl', editable=False)

class SSHCertificate(Certificate):
    authorized_keys = models.TextField()
    type = models.CharField(max_length=50, default='ssh', editable=False)

class CustomCertificate(Certificate):
    custom_field = models.CharField(max_length=255)
    custom_data = models.JSONField()
    type = models.CharField(max_length=50, default='custom', editable=False)

class ServiceProvider(ResourceBase):

    def __str__(self):
        return self.name

class Transport(ResourceBase):

    def __str__(self):
        return self.name

class VRF(ResourceBase):

    def __str__(self):
        return self.name

class MachineGroup(ResourceBase):
    compliance = models.CharField(max_length=255, verbose_name="Compliance Standard")

    def __str__(self):
        return self.name
    
class Machine(ResourceBase):
    DEVICE_TYPE_CHOICES = [
        ('laptop', 'Laptop'),
        ('phone', 'Phone'),
        ('tablet', 'Tablet'),
        ('network', 'Network Device'),
        ('other', 'Other')
    ]
    OS_CHOICES = [
        ('windows', 'Windows'),
        ('linux', 'Linux'),
        ('mac_os', 'Mac OS'),
        ('ios', 'iOS'),
        ('android', 'Android')
    ]

    device_group = models.ForeignKey('MachineGroup', on_delete=models.CASCADE, related_name='devices_device_group')
    type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os = models.CharField(max_length=50, choices=OS_CHOICES)
    serial_number = models.CharField(max_length=255)
    certificate = models.URLField()
    trusted_ca = models.URLField()
    admins = models.JSONField()
    users = models.JSONField()

    def __str__(self):
        return self.name
    
class DSNDevice(ResourceBase):
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    software = models.CharField(max_length=255, verbose_name="Software Version")
    serial_number = models.CharField(max_length=255)
    certificate = models.URLField()
    trusted_ca = models.URLField()
    descriptions = models.TextField(blank=True, null=True)
    registered = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Server(BasePolymorphic):
    address = models.CharField(max_length=100)
    fqdn = models.CharField(max_length=255)
    tls_enabled = models.BooleanField(default=False)
    tls_certificate = models.CharField(max_length=100, blank=True, null=True)
    tls_key = models.CharField(max_length=100, blank=True, null=True)
    ca_certificate = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class CustomServer(Server):
    type = models.CharField(max_length=50, default='custom', editable=False)
    custom_data = JSONField()

    def save(self, *args, **kwargs):
        self.type = 'custom'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SyslogServer(Server):
    port = models.IntegerField()
    transport_protocol = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.type = 'syslog'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NTPServer(Server):
    version = models.IntegerField()
    auth_key = models.CharField(max_length=100, blank=True, null=True)
    max_poll = models.IntegerField()
    min_poll = models.IntegerField()

    def save(self, *args, **kwargs):
        self.type = 'ntp'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.address

class DNSServer(Server):
    dnssec_active = models.BooleanField(default=False)
    unsigned_check = models.BooleanField(default=False)
    timecheck = models.BooleanField(default=False)
    dnssec_class = models.CharField(max_length=50, blank=True, null=True)
    key_tag = models.CharField(max_length=50, blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    digest_type = models.CharField(max_length=10, blank=True, null=True)
    digest = models.CharField(max_length=255, blank=True, null=True)
    public_key = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type = 'dns'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class LDAPServer(Server):
    base_dn = models.CharField(max_length=255)
    port = models.IntegerField(default=389)
    use_ssl = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.type = 'ldap'
        super().save(*args, **kwargs)

class RADIUSServer(Server):
    secret = models.CharField(max_length=255)
    auth_port = models.IntegerField(default=1812)
    acct_port = models.IntegerField(default=1813)

    def save(self, *args, **kwargs):
        self.type = 'radius'
        super().save(*args, **kwargs)

class FileServer(Server):
    storage_capacity = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.type = 'file'
        super().save(*args, **kwargs)

class WebServer(Server):
    technology = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.type = 'web'
        super().save(*args, **kwargs)

class ActiveDirectoryServer(Server):
    domain = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.type = 'ad'
        super().save(*args, **kwargs)

class AzureADServer(Server):
    tenant_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    redirect_uri = models.URLField(max_length=1024, blank=True, null=True)
    domain = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.type = 'azure_ad'
        super().save(*args, **kwargs)

class IdPServer(Server):
    entity_id = models.CharField(max_length=255)
    sso_url = models.URLField(max_length=1024, blank=True, null=True)
    slo_url = models.URLField(max_length=1024, blank=True, null=True)
    public_cert = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    metadata_url = models.URLField(max_length=1024, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type = 'idp'
        super().save(*args, **kwargs)

class IPFixCollector(Server):
    protocol = models.IntegerField()
    port = models.IntegerField()

    def save(self, *args, **kwargs):
        self.type = 'collector'
        super().save(*args, **kwargs)