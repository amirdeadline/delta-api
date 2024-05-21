# tenants_app/views.py
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import (Product, ProductCategory, License, Region, SCE, SASEController,
                     SDWANController, Contact, Customer, AdminUser, Tenant, ShareTag,
                     IKEEncryption, IKEHash, IKEDHGroup, IKERPF, ESPEncryption, DeletedTenant,
                     InterfaceType, InterfaceRole, VRFRole, LACPHashOption, DeviceModel,
                     ESPHash, ESPDHGroup, ESPPFS, RoutingProtocol, Domain, SDWANSoftware)
from .serializers import (ProductSerializer, ProductCategorySerializer, LicenseSerializer,
                          RegionSerializer, SCESerializer, SASEControllerSerializer,
                          SDWANControllerSerializer, ContactSerializer, CustomerSerializer,
                          AdminUserSerializer, TenantSerializer, ShareTagSerializer,
                          IKEEncryptionSerializer, IKEHashSerializer, IKEDHGroupSerializer,
                          IKERPFSerializer, ESPEncryptionSerializer, ESPHashSerializer,
                          InterfaceTypeSerializer, InterfaceRoleSerializer, VRFRoleSerializer, LACPHashOptionSerializer, DeviceModelSerializer,
                          ESPDHGroupSerializer, ESPPFSSerializer, RoutingProtocolSerializer, SDWANSoftwareSerializer)
import psycopg2
from django.db import connection
# from django.db.utils import ProgrammingError
# from .default_settings import copy_data_from_default
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def perform_create(self, serializer):
        try:
            tenant = serializer.save()  # Create the tenant
            domain = Domain(domain=str(tenant.tenant_id), tenant=tenant, is_primary=True)
            domain.save()
            # copy_data_from_default(tenant)  # Uncomment and handle this properly
            
            # self.create_initial_tenant_setting(tenant.schema_name)
            logger.info(f"Created new Tenant {tenant.name} with domain {domain.domain}")
        except Exception as e:
            logger.error(f"Failed to create tenant or domain: {str(e)}")
            raise serializers.ValidationError("Failed to create tenant or domain")
    @transaction.atomic
    def perform_destroy(self, instance):
        try:
            logger.info(f"Attempting to delete tenant: {instance.name}")
            DeletedTenant.objects.create(
                tenant_id=instance.tenant_id,
                schema_name=instance.schema_name,
                name=instance.name,
                description=instance.description,
                deleted_by=self.request.user_id,
                deleted_at=timezone.now(),
                customer=instance.customer,
                config=instance.config,
                snapshot=instance.snapshot,
                detail=instance.detail
            )
            # This deletes the domain and tenant, including dropping the schema if auto_drop_schema is True
            instance.domains.all().delete()  # Clean up related domains first
            instance.delete()  # This should also drop the schema due to auto_drop_schema being True
            logger.info(f"Hard deleted tenant {instance.name} and its schema.")
        except Exception as e:
            logger.error(f"Failed to delete tenant {instance.name}: {str(e)}")
            raise serializers.ValidationError("Failed to delete tenant")

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        tenant = self.get_object()
        children = TenantSerializer(tenant.get_children(), many=True).data
        return Response(children, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(TenantViewSet, self).get_serializer_context()
        context['user_id'] = self.request.user_id  # Assuming `user_id` is set in the request by middleware
        return context

class SDWANSoftwareViewSet(viewsets.ModelViewSet):
    queryset = SDWANSoftware.objects.all()
    serializer_class = SDWANSoftwareSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ShareTagViewSet(viewsets.ModelViewSet):
    queryset = ShareTag.objects.all()
    serializer_class = ShareTagSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class SCEViewSet(viewsets.ModelViewSet):
    queryset = SCE.objects.all()
    serializer_class = SCESerializer

class SASEControllerViewSet(viewsets.ModelViewSet):
    queryset = SASEController.objects.all()
    serializer_class = SASEControllerSerializer

class SDWANControllerViewSet(viewsets.ModelViewSet):
    queryset = SDWANController.objects.all()
    serializer_class = SDWANControllerSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer

class IKEEncryptionViewSet(viewsets.ModelViewSet):
    queryset = IKEEncryption.objects.all()
    serializer_class = IKEEncryptionSerializer

class IKEHashViewSet(viewsets.ModelViewSet):
    queryset = IKEHash.objects.all()
    serializer_class = IKEHashSerializer

class IKEDHGroupViewSet(viewsets.ModelViewSet):
    queryset = IKEDHGroup.objects.all()
    serializer_class = IKEDHGroupSerializer

class IKERPFViewSet(viewsets.ModelViewSet):
    queryset = IKERPF.objects.all()
    serializer_class = IKERPFSerializer

class ESPEncryptionViewSet(viewsets.ModelViewSet):
    queryset = ESPEncryption.objects.all()
    serializer_class = ESPEncryptionSerializer

class ESPHashViewSet(viewsets.ModelViewSet):
    queryset = ESPHash.objects.all()
    serializer_class = ESPHashSerializer

class ESPDHGroupViewSet(viewsets.ModelViewSet):
    queryset = ESPDHGroup.objects.all()
    serializer_class = ESPDHGroupSerializer

class ESPPFSViewSet(viewsets.ModelViewSet):
    queryset = ESPPFS.objects.all()
    serializer_class = ESPPFSSerializer

class RoutingProtocolViewSet(viewsets.ModelViewSet):
    queryset = RoutingProtocol.objects.all()
    serializer_class = RoutingProtocolSerializer

class InterfaceTypeViewSet(viewsets.ModelViewSet):
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer

class InterfaceRoleViewSet(viewsets.ModelViewSet):
    queryset = InterfaceRole.objects.all()
    serializer_class = InterfaceRoleSerializer

class VRFRoleViewSet(viewsets.ModelViewSet):
    queryset = VRFRole.objects.all()
    serializer_class = VRFRoleSerializer

class LACPHashOptionViewSet(viewsets.ModelViewSet):
    queryset = LACPHashOption.objects.all()
    serializer_class = LACPHashOptionSerializer

class DeviceModelViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
