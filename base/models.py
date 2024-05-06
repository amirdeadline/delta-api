# base/models.py
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import uuid
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError 
import logging

logger = logging.getLogger(__name__)

class Tag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
    
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)s_tags")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        if not self.pk:  # Object is being created
            self.created_by = user_id
        self.modified_by = user_id
        if self.tags.count() > 5:
            raise ValidationError("Maximum number of tags exceeded (5 tags allowed).")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        self.deleted_at = timezone.now()
        self.deleted_by = user_id
        super().delete(*args, **kwargs)

class Secret(BaseModel):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    secret_id= should start with 9900 and then increasing 8 digit value and in total secret_id will be 12 digits

class AvailableOverlayIP(models.Model):
    address=models.GenericIPAddressField(protocol='ipv4', unique=True, primary_key=True)
    available = models.BooleanField(default=True)

class CandidateConfig(BaseModel):
    committed_at = models.DateTimeField(null=True, blank=True)
    committed_by = models.CharField(max_length=100, null=True, blank=True)
    committed = models.BooleanField(default=False)
    base_config = JSONField()
    config_changes = JSONField()

class SnapshotConfig(BaseModel):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    config = JSONField()

class Address(models.Model):
    street1 = models.CharField(max_length=255, verbose_name="Street Line 1")
    street2 = models.CharField(max_length=255, verbose_name="Street Line 2", blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, verbose_name="State/Province/Region")
    postal_code = models.CharField(max_length=20, verbose_name="Postal/ZIP Code")
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude")

    def __str__(self):
        return f"{self.street1}, {self.city}, {self.region}, {self.postal_code}, {self.country}"

class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="Full Name")
    phone1 = models.CharField(max_length=20, verbose_name="Primary Phone Number", blank=True, null=True)
    phone2 = models.CharField(max_length=20, verbose_name="Secondary Phone Number", blank=True, null=True)
    email = models.EmailField(verbose_name="Email Address", blank=True, null=True)
    url = models.URLField(verbose_name="Website URL", blank=True, null=True)

    def __str__(self):
        return self.name

class TenantSetting(models.Model):
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    infra_subnet = models.GenericIPAddressField(protocol='IPv4', verbose_name="Infrastructure Subnet", blank=True, null=True)
    sase_bgp_asn = models.PositiveIntegerField(verbose_name="SASE BGP ASN", blank=True, null=True)
    sdwan_bgp_asn = models.PositiveIntegerField(verbose_name="SD-WAN BGP ASN", blank=True, null=True)
    sase_community = models.CharField(max_length=255, verbose_name="SASE Community", blank=True, null=True)
    sdwan_community = models.CharField(max_length=255, verbose_name="SD-WAN Community", blank=True, null=True)
