# base/models.py
from django.db import models, router
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from tenants_app.models import Tenant
from django.db import transaction
import ipaddress
from delta_api.celery import app as celery_app
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,MaxValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)
    # value = JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created", null=True, blank=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, related_name="%(class)s_modified", null=True, blank=True, on_delete=models.SET_NULL)
    deleted_by = models.ForeignKey(User, related_name="%(class)s_deleted", null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)  # A set of related tags

    class Meta:
        abstract = True