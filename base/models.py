# base/models.py
from django.db import models
from django.db.models import JSONField
import uuid
import time
import random
from threading import Lock
from django.core.exceptions import ValidationError 
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

sequence_lock = Lock()
last_timestamp = None
sequence_number = 0

OBJECT_TYPE_CODES = {
    'BaseModel': '00000',  # Override in subclasses with specific codes
    'ooo': '00001',
}

def generate_unique_id(object_type):
    object_prefix = OBJECT_TYPE_CODES.get(object_type, '00000')
    current_timestamp = int(time.time() * 1000)
    sequence_number = random.randint(0, 99)
    unique_id = f"{object_prefix}{current_timestamp:010}{MACHINE_ID}{sequence_number:02}"
    return unique_id[:17]

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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, )
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)s_tags")
    object_id = models.CharField(max_length=16, unique=True, editable=False, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        if not self.pk:  # Object is being created
            self.created_by = user_id
        self.modified_by = user_id
        if self.tags.count() > 5:
            raise ValidationError("Maximum number of tags exceeded (5 tags allowed).")
        if not self.object_id:
            # Using the class name as the object type for ID generation
            self.object_id = generate_unique_id(self.__class__.__name__)
        super().save(*args, **kwargs)


class BasePolymorphic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, )
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)s_tags")
    object_id = models.CharField(max_length=16, unique=True, editable=False, db_index=True)
    objects = PolymorphicManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Receive user_id from the view
        if not self.pk:  # Object is being created
            self.created_by = user_id
        self.modified_by = user_id
        if self.tags.count() > 5:
            raise ValidationError("Maximum number of tags exceeded (5 tags allowed).")
        if not self.object_id:
            # Using the class name as the object type for ID generation
            self.object_id = generate_unique_id(self.__class__.__name__)
        super().save(*args, **kwargs)



class AvailableOverlayIP(models.Model):
    address=models.GenericIPAddressField(protocol='ipv4', unique=True, primary_key=True)

class CandidateConfig(BaseModel):
    committed_at = models.DateTimeField(null=True, blank=True, db_index=True)
    committed_by = models.CharField(max_length=100, null=True, blank=True)
    committed = models.BooleanField(default=False)
    base_config = JSONField()
    config_changes = JSONField()

class SnapshotConfig(BaseModel):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    config = JSONField()

# class Address(models.Model):
#     street1 = models.CharField(max_length=255, verbose_name="Street Line 1", blank=True, null=True)
#     street2 = models.CharField(max_length=255, verbose_name="Street Line 2", blank=True, null=True)
#     city = models.CharField(max_length=100)
#     region = models.CharField(max_length=100, verbose_name="State/Province/Region")
#     postal_code = models.CharField(max_length=20, verbose_name="Postal/ZIP Code")
#     country = models.CharField(max_length=100)
#     latitude = models.FloatField(null=True, blank=True, help_text="Latitude")
#     longitude = models.FloatField(null=True, blank=True, help_text="Longitude")

#     def __str__(self):
#         return f"{self.street1}, {self.city}, {self.region}, {self.postal_code}, {self.country}"

# class Contact(models.Model):
#     name = models.CharField(max_length=255, verbose_name="Full Name",db_index=True)
#     phone1 = models.CharField(max_length=20, verbose_name="Primary Phone Number", blank=True, null=True)
#     phone2 = models.CharField(max_length=20, verbose_name="Secondary Phone Number", blank=True, null=True)
#     email = models.EmailField(verbose_name="Email Address", blank=True, null=True)
#     url = models.URLField(verbose_name="Website URL", blank=True, null=True)

#     def __str__(self):
#         return self.name

class TenantSetting(models.Model):
    key = models.CharField(max_length=100, primary_key=True, unique=True, db_index=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"
