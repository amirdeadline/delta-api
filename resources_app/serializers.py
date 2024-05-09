# resources_app/serializers.py
from rest_framework import serializers
from .models import ResourceBase, Certificate, CACertificate, SSLCertificate, SSHCertificate, CustomCertificate, ServiceProvider, Transport, VRF, MachineGroup, Machine, DSNDevice, Server, CustomServer, SyslogServer, NTPServer, DNSServer, LDAPServer, RADIUSServer, FileServer, WebServer, ActiveDirectoryServer, AzureADServer, IdPServer, IPFixCollector
from base.serializers import BaseModelSerializer

class ResourceBaseSerializer(BaseModelSerializer):
    class Meta:
        model = ResourceBase

class CertificateSerializer(ResourceBaseSerializer):
    class Meta:
        model = Certificate

class CACertificateSerializer(CertificateSerializer):
    class Meta:
        model = CACertificate

class SSLCertificateSerializer(CertificateSerializer):
    class Meta:
        model = SSLCertificate

class SSHCertificateSerializer(CertificateSerializer):
    class Meta:
        model = SSHCertificate

class CustomCertificateSerializer(CertificateSerializer):
    class Meta:
        model = CustomCertificate

class ServiceProviderSerializer(ResourceBaseSerializer):
    class Meta:
        model = ServiceProvider

class TransportSerializer(ResourceBaseSerializer):
    class Meta:
        model = Transport

class VRFSerializer(ResourceBaseSerializer):
    class Meta:
        model = VRF

class MachineGroupSerializer(ResourceBaseSerializer):
    class Meta:
        model = MachineGroup

class MachineSerializer(ResourceBaseSerializer):
    class Meta:
        model = Machine

class DSNDeviceSerializer(ResourceBaseSerializer):
    class Meta:
        model = DSNDevice

class ServerSerializer(ResourceBaseSerializer):
    class Meta:
        model = Server

class CustomServerSerializer(ServerSerializer):
    class Meta:
        model = CustomServer

class SyslogServerSerializer(ServerSerializer):
    class Meta:
        model = SyslogServer

class NTPServerSerializer(ServerSerializer):
    class Meta:
        model = NTPServer

class DNSServerSerializer(ServerSerializer):
    class Meta:
        model = DNSServer

class LDAPServerSerializer(ServerSerializer):
    class Meta:
        model = LDAPServer

class RADIUSServerSerializer(ServerSerializer):
    class Meta:
        model = RADIUSServer

class FileServerSerializer(ServerSerializer):
    class Meta:
        model = FileServer

class WebServerSerializer(ServerSerializer):
    class Meta:
        model = WebServer

class ActiveDirectoryServerSerializer(ServerSerializer):
    class Meta:
        model = ActiveDirectoryServer

class AzureADServerSerializer(ServerSerializer):
    class Meta:
        model = AzureADServer

class IdPServerSerializer(ServerSerializer):
    class Meta:
        model = IdPServer

class IPFixCollectorSerializer(ServerSerializer):
    class Meta:
        model = IPFixCollector
