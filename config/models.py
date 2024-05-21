# config_app/models.py
from django.db import models
from django.db.models import JSONField
from datetime import datetime
from base.models import BaseModel
import logging

logger = logging.getLogger(__name__)

class ConfigBase(BaseModel):
    """"
    This model is abstract inherits all feilds from BASE MODEL in Base app
    """
    name = models.CharField(max_length=255, blank=True)

class SnapshotConfig(ConfigBase):
    # name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.name:  # Generate name if not provided
            now = datetime.now()
            self.name = f"Snapshot_{now.strftime('%m%d%y_%H%M%S')}"
        super().save(*args, **kwargs)

class CandidateConfig(ConfigBase):
    # name = models.CharField(max_length=255, blank=True)
    committed_at = models.DateTimeField(null=True, blank=True, db_index=True)
    committed_by = models.CharField(max_length=100, null=True, blank=True)
    committed = models.BooleanField(default=False)
    base_snapshot = models.ForeignKey(SnapshotConfig, on_delete=models.PROTECT, related_name="base_snapshots")
    changes = JSONField(default=dict) 

    def save(self, *args, **kwargs):
        if not self.name:  # Generate name if not provided
            now = datetime.now()
            self.name = f"Candidate_{now.strftime('%m%d%y_%H%M%S')}"
        if not self.pk:  # Check if it's a new instance
            snapshot = SnapshotConfig.objects.create(path="root/")
            self.base_snapshot = snapshot
        super().save(*args, **kwargs)