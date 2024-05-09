from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SSLCertificateViewSet, SSHCertificateViewSet, CustomCertificateViewSet,
    ServiceProviderViewSet, TransportViewSet, VRFViewSet, MachineGroupViewSet,
    MachineViewSet, DSNDeviceViewSet, ServerViewSet, CustomServerViewSet,
    SyslogServerViewSet, NTPServerViewSet, DNSServerViewSet, LDAPServerViewSet,
    RADIUSServerViewSet, FileServerViewSet, WebServerViewSet,
    ActiveDirectoryServerViewSet, AzureADServerViewSet, CACertificateViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'certificates/cacertificates', CACertificateViewSet)
router.register(r'certificates/sslcertificates', SSLCertificateViewSet)
router.register(r'certificates/sshcertificates', SSHCertificateViewSet)
router.register(r'certificates/customcertificates', CustomCertificateViewSet)
router.register(r'serviceproviders', ServiceProviderViewSet)
router.register(r'transports', TransportViewSet)
router.register(r'vrfs', VRFViewSet)
router.register(r'machinegroups', MachineGroupViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'dsndevices', DSNDeviceViewSet)
router.register(r'servers', ServerViewSet)
router.register(r'customservers', CustomServerViewSet)
router.register(r'syslogservers', SyslogServerViewSet)
router.register(r'ntpservers', NTPServerViewSet)
router.register(r'dnsservers', DNSServerViewSet)
router.register(r'ldapservers', LDAPServerViewSet)
router.register(r'radiusservers', RADIUSServerViewSet)
router.register(r'fileservers', FileServerViewSet)
router.register(r'webservers', WebServerViewSet)
router.register(r'activedirectoryservers', ActiveDirectoryServerViewSet)
router.register(r'azureadservers', AzureADServerViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
