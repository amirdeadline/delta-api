# resources_app/views.py
from rest_framework import viewsets
from .models import CACertificate, SSLCertificate, SSHCertificate, CustomCertificate, ServiceProvider, Transport, VRF, MachineGroup, Machine, DSNDevice, Server, CustomServer, SyslogServer, NTPServer, DNSServer, LDAPServer, RADIUSServer, FileServer, WebServer, ActiveDirectoryServer, AzureADServer, IdPServer, IPFixCollector
from .serializers import CACertificateSerializer, SSLCertificateSerializer, SSHCertificateSerializer, CustomCertificateSerializer, ServiceProviderSerializer, TransportSerializer, VRFSerializer, MachineGroupSerializer, MachineSerializer, DSNDeviceSerializer, ServerSerializer, CustomServerSerializer, SyslogServerSerializer, NTPServerSerializer, DNSServerSerializer, LDAPServerSerializer, RADIUSServerSerializer, FileServerSerializer, WebServerSerializer, ActiveDirectoryServerSerializer, AzureADServerSerializer, IdPServerSerializer, IPFixCollectorSerializer
from base.views import BaseModelViewSet

class CACertificateViewSet(BaseModelViewSet):
    queryset = CACertificate.objects.all()
    serializer_class = CACertificateSerializer

class SSLCertificateViewSet(BaseModelViewSet):
    queryset = SSLCertificate.objects.all()
    serializer_class = SSLCertificateSerializer

class SSHCertificateViewSet(BaseModelViewSet):
    queryset = SSHCertificate.objects.all()
    serializer_class = SSHCertificateSerializer

class CustomCertificateViewSet(BaseModelViewSet):
    queryset = CustomCertificate.objects.all()
    serializer_class = CustomCertificateSerializer

class ServiceProviderViewSet(BaseModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class TransportViewSet(BaseModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer

class VRFViewSet(BaseModelViewSet):
    queryset = VRF.objects.all()
    serializer_class = VRFSerializer

class MachineGroupViewSet(BaseModelViewSet):
    queryset = MachineGroup.objects.all()
    serializer_class = MachineGroupSerializer

class MachineViewSet(BaseModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class DSNDeviceViewSet(BaseModelViewSet):
    queryset = DSNDevice.objects.all()
    serializer_class = DSNDeviceSerializer

class ServerViewSet(BaseModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class CustomServerViewSet(BaseModelViewSet):
    queryset = CustomServer.objects.all()
    serializer_class = CustomServerSerializer

class SyslogServerViewSet(BaseModelViewSet):
    queryset = SyslogServer.objects.all()
    serializer_class = SyslogServerSerializer

class NTPServerViewSet(BaseModelViewSet):
    queryset = NTPServer.objects.all()
    serializer_class = NTPServerSerializer

class DNSServerViewSet(BaseModelViewSet):
    queryset = DNSServer.objects.all()
    serializer_class = DNSServerSerializer

class LDAPServerViewSet(BaseModelViewSet):
    queryset = LDAPServer.objects.all()
    serializer_class = LDAPServerSerializer

class RADIUSServerViewSet(BaseModelViewSet):
    queryset = RADIUSServer.objects.all()
    serializer_class = RADIUSServerSerializer

class FileServerViewSet(BaseModelViewSet):
    queryset = FileServer.objects.all()
    serializer_class = FileServerSerializer

class WebServerViewSet(BaseModelViewSet):
    queryset = WebServer.objects.all()
    serializer_class = WebServerSerializer

class ActiveDirectoryServerViewSet(BaseModelViewSet):
    queryset = ActiveDirectoryServer.objects.all()
    serializer_class = ActiveDirectoryServerSerializer

class AzureADServerViewSet(BaseModelViewSet):
    queryset = AzureADServer.objects.all()
    serializer_class = AzureADServerSerializer

