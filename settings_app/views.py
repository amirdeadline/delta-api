# settings_app/views.py
from rest_framework import viewsets
from .models import TenantSetting, SASEInfraSubnet
from .serializers import TenantSettingSerializer, SASEInfraSubnetSerializer
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
import logging

logger = logging.getLogger(__name__)

class SASEInfraSubnetViewSet(viewsets.ModelViewSet):
    queryset = SASEInfraSubnet.objects.all()
    serializer_class = SASEInfraSubnetSerializer

class TenantSettingViewSet(viewsets.ModelViewSet):
    queryset = TenantSetting.objects.all()
    serializer_class = SASEInfraSubnetSerializer