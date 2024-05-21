#settings_app/models.py
from django.db import models
import ipaddress
from netaddr import IPNetwork
from django.core.exceptions import ValidationError

def validate_cidr(value):
    # Validate that the value is a proper CIDR notation
    try:
        new_subnet = ipaddress.ip_network(value, strict=False)
    except ValueError:
        raise ValidationError(f"{value} is not a valid CIDR notation")

    # Retrieve all existing subnets from the database
    all_subnets = SASEInfraSubnet.objects.values_list('subnet', flat=True)
    
    # Check for conflicts with existing subnets
    for subnet_str in all_subnets:
        existing_subnet = ipaddress.ip_network(subnet_str, strict=False)
        if new_subnet.overlaps(existing_subnet):
            raise ValidationError(f"Subnet {value} has conflict with existing subnet {subnet_str}")

class SASEInfraSubnet(models.Model):
    subnet = models.CharField(max_length=255, validators=[validate_cidr])
    tags= models.JSONField(default=dict)

class TenantSetting(models.Model):
    description = models.TextField(verbose_name="Description", default="")
    sase_bgp_asn = models.PositiveIntegerField(verbose_name="SASE BGP ASN", default=64512)
    sdwan_bgp_asn = models.PositiveIntegerField(verbose_name="SD-WAN BGP ASN", default=64513)
    sase_community = models.CharField(max_length=255, verbose_name="SASE Community", default='64512:1')
    sdwan_community = models.CharField(max_length=255, verbose_name="SD-WAN Community", default='64513:1')

    def save(self, *args, **kwargs):
        if TenantSetting.objects.exists() and not self.pk:
            raise ValidationError("Please Use PATCH call to change Tenant Settings")
        super().save(*args, **kwargs)