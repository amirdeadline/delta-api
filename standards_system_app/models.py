# standards_system_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator
from resources_app.models import Certificate, SyslogServer, NTPServer, IPFixCollector, SNMPServer, DNSServer

import logging

logger = logging.getLogger(__name__)

class SysStandardTag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
        
class SysStandardBase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags = models.ManyToManyField(SysStandardTag, blank=True, related_name="%(class)s_tags")
    detail = JSONField()
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

class SyslogStandard(SysStandardBase):
    enabled = models.BooleanField(default=True)
    facility = models.CharField(max_length=50)
    severity = models.CharField(max_length=50)
    servers = models.ManyToManyField(SyslogServer, related_name='syslog_standards')
    def __str__(self):
        return self.name

class IPFIXStandard(SysStandardBase):
    export_interval = models.IntegerField(help_text='Interval in seconds')
    transport_protocol = models.CharField(max_length=10)
    template_refresh_time = models.IntegerField(help_text='Template refresh time in seconds')
    option_template = models.BooleanField(default=True)
    record_fields = models.TextField(help_text='Comma-separated record fields')
    collectors = models.ManyToManyField(IPFixCollector, related_name='ipfix_standards_collectors')

    def __str__(self):
        return self.name

class SNMPStandard(SysStandardBase):
    version = models.CharField(max_length=10)
    community_string = models.CharField(max_length=100, blank=True, null=True)
    authentication_protocol = models.CharField(max_length=50, blank=True, null=True)
    authentication_password = models.CharField(max_length=100, blank=True, null=True)
    encryption_protocol = models.CharField(max_length=50, blank=True, null=True)
    encryption_password = models.CharField(max_length=100, blank=True, null=True)
    security_level = models.CharField(max_length=50, blank=True, null=True)
    trap_receiver_port = models.IntegerField()
    engine_id = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    trap_receiver_ip = models.CharField(max_length=100)
    trap_receiver_port = models.IntegerField()

    def __str__(self):
        return self.name
    
class NTPStandard(SysStandardBase):
    server1 = models.ForeignKey(NTPServer, on_delete=models.PROTECT, )
    server2 = models.ForeignKey(NTPServer, on_delete=models.SET_NULL, null=True)
    server3 = models.ForeignKey(NTPServer, on_delete=models.SET_NULL, null=True)
    server4 = models.ForeignKey(NTPServer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class DNSService(SysStandardBase):
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



