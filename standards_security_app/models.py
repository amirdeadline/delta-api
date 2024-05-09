# standards_security_app/models.py
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

class SecStandardTag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
        
class SecStandardBase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags = models.ManyToManyField(SecStandardTag, blank=True, related_name="%(class)s_tags")
    detail = JSONField(default=dict)
    enabled = models.BooleanField(default=True)
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

class AntivirusStandard(SecStandardBase):
    description = models.TextField(blank=True, null=True)
        # Scan settings
    scan_on_access = models.BooleanField(default=True)
    scan_on_write = models.BooleanField(default=True)
    scan_on_read = models.BooleanField(default=True)
       # Threat handling
    block_threats = models.BooleanField(default=True)
    quarantine_infected_files = models.BooleanField(default=True)
    # Update settings
    update_signatures_automatically = models.BooleanField(default=True)
    # Logging
    log_all_scanned_traffic = models.BooleanField(default=True)
    log_block_actions = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DLPStandard(SecStandardBase):    # Basic profile information
    enable_monitoring = models.BooleanField(default=True)
    enable_prevention = models.BooleanField(default=True)
    content_inspection_data_types = ArrayField(models.CharField(max_length=100), blank=True)

    network_protection_protocols = ArrayField(models.CharField(max_length=10), blank=True)
    inspect_encrypted_traffic = models.BooleanField(default=True)
    endpoint_protection_monitor_clipboard = models.BooleanField(default=True)
    endpoint_protection_block_transfers = ArrayField(models.CharField(max_length=50), blank=True)
    storage_protection_cloud_storage = ArrayField(models.CharField(max_length=100), blank=True)
    storage_protection_actions = ArrayField(models.CharField(max_length=50), blank=True)


    def __str__(self):
        return self.name

class DLPContentInspect(models.Model):
    dlp_standard = models.ForeignKey(DLPStandard, on_delete=models.CASCADE)
    deep_inspection = models.BooleanField(default=True)
    actions = ArrayField(models.CharField(max_length=50), blank=True)
    exceptions = JSONField(default=dict, blank=True, null=True)

class DLPNetworkProtection(models.Model):
    dlp_standard = models.ForeignKey(DLPStandard, on_delete=models.CASCADE)
    protocols = ArrayField(models.CharField(max_length=10), blank=True)
    inspection_encrypted_traffic = models.BooleanField(default=True)
    actions = ArrayField(models.CharField(max_length=50), blank=True)
    exceptions = JSONField(default=dict, blank=True, null=True)

class DLPEndPointProtection(models.Model):
    dlp_standard = models.ForeignKey(DLPStandard, on_delete=models.CASCADE)
    monitor_clipboard = models.BooleanField(default=True)
    block_transfers = ArrayField(models.CharField(max_length=50), blank=True)
    actions = ArrayField(models.CharField(max_length=50), blank=True)
    exceptions = JSONField(default=dict, blank=True, null=True)

class DLPStorageProtection(models.Model):
    dlp_standard = models.ForeignKey(DLPStandard, on_delete=models.CASCADE)
    cloud_storage = ArrayField(models.CharField(max_length=100), blank=True)
    actions = ArrayField(models.CharField(max_length=50), blank=True)
    exceptions = JSONField(default=dict, blank=True, null=True)