# standards_service_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator
from resources_app.models import Certificate ,DNSServer

import logging

logger = logging.getLogger(__name__)

class ServStandardTag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
        
class ServStandardBase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags = models.ManyToManyField(ServStandardTag, blank=True, related_name="%(class)s_tags")
    detail = JSONField(default=dict)
    enabled = models.BooleanField(default=True)
    source_address_tag = models.CharField(max_length=100, blank=True, null=True)
    source_interface_tag = models.CharField(max_length=100, blank=True, null=True)
    logging = models.BooleanField(default=False)

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

class DNSService(ServStandardBase):
    caching = models.BooleanField(default=True)
    port = models.IntegerField(default=53)
    interface_tag = models.JSONField(blank=True, null=True)
    address_tag = models.CharField(max_length=100, blank=True, null=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.SET_NULL, null=True, related_name='dnsservices')
    forwarding_servers = models.ManyToManyField(DNSServer, on_delete=models.PROTECT, related_name='dnsservice_servers')
    cache_size = models.CharField(max_length=50)
    max_ttl = models.IntegerField(help_text='Maximum time to live for DNS records')
    min_ttl = models.IntegerField(help_text='Minimum time to live for DNS records')
    neg_ttl = models.IntegerField(help_text='Negative caching time to live')
    max_entries = models.IntegerField(help_text='Maximum number of cache entries')
    static_entries = models.JSONField(blank=True, null=True)  # Storing static DNS entries as JSON

    def __str__(self):
        return self.name

class DHCPRelayStandard(ServStandardBase):
    servers = JSONField(default=dict) #it should be json with priority as key and server address as value
    options = models.JSONField(default=dict, help_text="Additional DHCP options in JSON format")

    def __str__(self):
        return self.name

class DHCPServerStandard(ServStandardBase):
    ip_start_count = models.GenericIPAddressField(blank=True, null=True, help_text="Exclude count from Start")
    ip_end_count = models.GenericIPAddressField(blank=True, null=True, help_text="Exclude count from End")
    ip_start_percent = models.GenericIPAddressField(blank=True, null=True, help_text="percent of subnet exclud from end")
    ip_end_percent = models.GenericIPAddressField(blank=True, null=True, help_text="percent of subnet exclud from end")
    default_gateway_self = models.BooleanField(default=True)
    dns_self = models.BooleanField(default=True)
    lease_time = models.IntegerField(default=86400, help_text="Lease time in seconds")
    dns_servers = models.ManyToManyField(DNSServer, on_delete=models.PROTECT, related_name='dnsservice_servers')
    wins_servers = models.CharField(max_length=255, blank=True, help_text="Comma-separated WINS servers")
    options = models.JSONField(default=dict, help_text="Additional DHCP options in JSON format")

    def __str__(self):
        return self.name