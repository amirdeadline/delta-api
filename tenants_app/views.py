# tenants_app/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Tenant, Domain
from .serializers import CustomerSerializer, TenantSerializer
from django.db import connection
from django.db.utils import ProgrammingError
import logging
from .default_settings import copy_data_from_default

logger = logging.getLogger(__name__)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def perform_create(self, serializer):
        logger.info("Creating a new Tenant")
        tenant = serializer.save()  # create the tenant

        # create an associated Domain for the tenant
        domain = Domain()
        domain.domain = tenant.tenant_id
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()
        # copy_data_from_default(tenant)
        logger.info(f"Created new Tenant {tenant.name} with domain {domain.domain}")

    def perform_destroy(self, instance):
        # Delete associated Domain instances.
        instance.domains.all().delete()
        
        # Drop the tenant's schema.
        instance.delete(force_drop=True)

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        tenant = self.get_object()
        children = TenantSerializer(tenant.get_children(), many=True).data
        return Response(children, status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

