# settings_app/serializers.py
from rest_framework import serializers
from .models import TenantSetting, SASEInfraSubnet

import logging

logger = logging.getLogger(__name__)


class SASEInfraSubnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SASEInfraSubnet
        exclude = ['id']

class TenantSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSetting
        exclude = ['id']