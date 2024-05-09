# standards_network_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator

import logging

logger = logging.getLogger(__name__)

class NetStandardTag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
        
class NetStandardBase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags = models.ManyToManyField(NetStandardTag, blank=True, related_name="%(class)s_tags")
    detail = JSONField()

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

class SLAStandard(NetStandardBase):
    interval = models.IntegerField(help_text='Interval in seconds', blank=True, null=True)
    threshold = models.FloatField(help_text='Threshold value', blank=True, null=True)
    wait_time = models.IntegerField(help_text='Wait time in seconds', blank=True, null=True)
    loss = models.FloatField(help_text='Acceptable packet loss percentage', blank=True, null=True)
    jitter = models.FloatField(help_text='Acceptable jitter in milliseconds', blank=True, null=True)
    mos = models.FloatField(help_text='Minimum Mean Opinion Score (MOS)', blank=True, null=True)

    def __str__(self):
        return self.name

class UnderlayStandard(NetStandardBase):
    up_bw = models.IntegerField(help_text='Upstream bandwidth in Mbps', blank=True, null=True)
    down_bw = models.IntegerField(help_text='Downstream bandwidth in Mbps', blank=True, null=True)
    shaping = models.BooleanField(default=False)
    metered = models.BooleanField(default=False)
    transport = models.CharField(max_length=50, blank=True, null=True)
    sla_target = models.CharField(max_length=100, blank=True, null=True)
    sla_standard = models.ForeignKey(SLAStandard, on_delete=models.SET_NULL, null=True, blank=True, related_name='underlays')

    def __str__(self):
        return self.name

class IPsecStandard(NetStandardBase):
    encryption_algorithm = models.CharField(max_length=50, blank=True, null=True)
    integrity_algorithm = models.CharField(max_length=50, blank=True, null=True)
    dh_group = models.CharField(max_length=50, blank=True, null=True)
    pfs_group = models.CharField(max_length=50, blank=True, null=True)
    lifetime_seconds = models.IntegerField(help_text='Lifetime of the security association in seconds', blank=True, null=True)
    lifetime_kilobytes = models.IntegerField(help_text='Lifetime of the security association in kilobytes', blank=True, null=True)

    def __str__(self):
        return self.name
    
class IKEStandard(NetStandardBase):
    description = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=2, help_text='IKE version')
    authentication_method = models.CharField(max_length=100, blank=True, null=True)
    psk = models.CharField(max_length=100, blank=True, null=True, verbose_name='Pre-Shared Key')
    random_psk= models.BooleanField(default=False)
    local_identity = models.CharField(max_length=100, blank=True, null=True)
    remote_identity = models.CharField(max_length=100, blank=True, null=True)
    dh_group = models.CharField(max_length=50, blank=True, null=True)
    encryption_algorithm = models.CharField(max_length=100, blank=True, null=True)
    hash_algorithm = models.CharField(max_length=100, blank=True, null=True)
    lifetime_seconds = models.IntegerField(blank=True, null=True, help_text='Lifetime of the security association in seconds')
    mobike = models.BooleanField(default=False, help_text='Support for MOBIKE protocol')
    nat_t = models.BooleanField(default=True, help_text='Support for NAT Traversal')

    def __str__(self):
        return self.name
