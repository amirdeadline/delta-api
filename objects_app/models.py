# objects_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator
from base.models import BaseModel ,BasePolymorphic

import logging

logger = logging.getLogger(__name__)
        
class ObjectBase(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    detail = JSONField()

    class Meta:
        abstract = True

class ObjectPolymorphic(BasePolymorphic):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    detail = JSONField()

    class Meta:
        abstract = True
        
class Zone(ObjectBase):
    role= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Address(ObjectPolymorphic):
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AddressSubnet(Address):
    type = models.CharField(max_length=20, default='subnet')
    mask = models.CharField(max_length=3, blank=True, null=True)

class AddressRange(Address):
    type = models.CharField(max_length=20, default='range')
    end_address = models.CharField(max_length=255)
    
class AddressGroup(ObjectBase):
    addresses = models.ManyToManyField(Address)
    def __str__(self):
        return self.name
    
class URL(ObjectBase):
    url = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class URLGroup(ObjectBase):
    urls = models.ManyToManyField(URL)
    def __str__(self):
        return self.name
    
class PrefixList(ObjectBase):

    def __str__(self):
        return self.name

class PrefixListRule(models.Model):
    seq = models.PositiveIntegerField()
    permit = models.BooleanField(default=True)  # True for permit, False for deny
    prefix = models.CharField(max_length=255)  # Typically an IP address range in CIDR format
    ge = models.PositiveIntegerField(blank=True, null=True)  # Greater than or equal prefix length
    le = models.PositiveIntegerField(blank=True, null=True)  # Less than or equal prefix length
    prefix_list = models.ForeignKey(PrefixList, related_name='rules', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Application(ObjectBase):
    app_id = models.CharField(max_length=100)
    app_category = models.CharField(max_length=100)
    priority = models.IntegerField(validators=[MaxValueValidator(999999)])
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    urls = ArrayField(models.CharField(max_length=255), size=10, blank=True)  # Can have up to 10 URLs
    port = models.CharField(max_length=10)  # Stores only one port number
    protocol = models.CharField(max_length=10)  # Stores only one protocol
    packet_payload = models.TextField(blank=True, null=True)
    ssl_certificates = ArrayField(models.CharField(max_length=255), blank=True)
    user_agents = ArrayField(models.CharField(max_length=255), blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Optional reference to another Application

    def __str__(self):
        return self.name

class Secret(ObjectBase):
    path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name