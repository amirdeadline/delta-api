# tenants_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import CustomerViewSet, TenantViewSet
from .views import (TenantViewSet, SDWANSoftwareViewSet, CustomerViewSet, ShareTagViewSet,
                    ProductViewSet, ProductCategoryViewSet, LicenseViewSet, RegionViewSet,
                    SCEViewSet, SASEControllerViewSet, SDWANControllerViewSet, ContactViewSet,
                    AdminUserViewSet, IKEEncryptionViewSet, IKEHashViewSet, IKEDHGroupViewSet,
                    IKERPFViewSet, ESPEncryptionViewSet, ESPHashViewSet, ESPDHGroupViewSet,
                    ESPPFSViewSet, RoutingProtocolViewSet, InterfaceTypeViewSet,
                    InterfaceRoleViewSet, VRFRoleViewSet, LACPHashOptionViewSet, DeviceModelViewSet)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'tenants', TenantViewSet, basename='tenants')
router.register(r'sdwan/software', SDWANSoftwareViewSet)
router.register(r'products', ProductViewSet)
router.register(r'products/categories', ProductCategoryViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'licenses', LicenseViewSet)
router.register(r'network/regions', RegionViewSet)
router.register(r'network/sase/sces', SCEViewSet)
router.register(r'network/sase/controllers', SASEControllerViewSet)
router.register(r'network/sdwan/controllers', SDWANControllerViewSet)
router.register(r'users', AdminUserViewSet)
router.register(r'support/ike/encrypt', IKEEncryptionViewSet)
router.register(r'support/ike/hash', IKEHashViewSet)
router.register(r'support/ike/dh', IKEDHGroupViewSet)
router.register(r'support/ike/rpf', IKERPFViewSet)
router.register(r'support/esp/encrypt', ESPEncryptionViewSet)
router.register(r'support/esp/hash', ESPHashViewSet)
router.register(r'support/esp/dh', ESPDHGroupViewSet)
router.register(r'support/esp/pfs', ESPPFSViewSet)
router.register(r'support/protocols/routing', RoutingProtocolViewSet)
router.register(r'support/interfaces/types', InterfaceTypeViewSet)
router.register(r'support/interfaces/roles', InterfaceRoleViewSet)
router.register(r'support/vrf/role', VRFRoleViewSet)
router.register(r'support/lacp/hash', LACPHashOptionViewSet)
router.register(r'support/devices/models', DeviceModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
