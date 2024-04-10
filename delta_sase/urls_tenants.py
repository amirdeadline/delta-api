# delta_api project urls_tenants.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponseServerError


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('network/sites/', include('sites_app.urls')),
    # path('network/devices/', include('devices_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
    path('network/', include('network_app.urls')),
    # path('monitor/', include('monitor_app.urls')),
    path('profiles/', include('profiles_app.urls')),
    # path('objects/', include('objects_app.urls')),
    # path('templates/', include('templates_app.urls')),
    # path('settings/', include('settings_app.urls')),
    # path('policies/security', include('security_policies_app.urls')),
    # path('policies/qos', include('qos_policies_app.urls')),
    # path('policies/nat', include('nat_policies_app.urls')),
    # path('policies/routing', include('routing_policies_app.urls')),
    # path('policies/authentication', include('auth_policies_app.urls')),
    # path('policies/', include('policies_app.urls')),
    # path('policies/', include('policies_app.urls')),

    ]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from dashboard_app.views import DashboardViewSet
# from network_app.views import SiteGroupViewSet, ProviderViewSet, TransportViewSet
# from sites_app.views import SiteViewSet, UnderlayViewSet, SDWANOverlayViewSet, SASEOverlayViewSet
# from interfaces_app.views import InterfaceViewSet, HAClusterViewSet, DHCPServerViewSet, DHCPRelayViewSet
# from devices_app.views import DeviceViewSet
# from profiles_app.views import (
#     SlaProfileViewSet, UnderlayProfileViewSet, DHCPRelayProfileViewSet, DHCPOptionViewSet, DHCPServerProfileViewSet, 
#     SyslogProfileViewSet, SNMPProfileViewSet, BFDProfileViewSet, IPSecProfileViewSet, WireGuardProfileViewSet,IPFIXProfileViewSet)

# # Network subfolder L1
# network_router = DefaultRouter()
# network_router.register(r'sitegroups', SiteGroupViewSet, basename='sitegroup')
# network_router.register(r'sites', SiteViewSet, basename='sitegroup')
# network_router.register(r'devices', DeviceViewSet, basename='sitegroup')
# network_router.register(r'transports', TransportViewSet, basename='transport')
# network_router.register(r'providers', ProviderViewSet, basename='provider')
# network_router.register(r'overlays/sdwan', SDWANOverlayViewSet, basename='sdwanoverlay')
# network_router.register(r'overlays/sase', SASEOverlayViewSet, basename='saseoverlay')

# ## Sites level
# sites_router = routers.NestedSimpleRouter(network_router, r'sites', lookup='sites')
# sites_router.register(r'interfaces', InterfaceViewSet, basename='site_interaces')
# sites_router.register(r'underlays', UnderlayViewSet, basename='site_underlays')
# sites_router.register(r'ha', HAClusterViewSet, basename='site_ha')

# ### interfaces level
# interfaces_router = routers.NestedSimpleRouter(sites_router, r'interfaces', lookup='interfaces')
# interfaces_router.register(r'dhcp/server', DHCPServerViewSet, basename='interfaces_dhcp_servers')
# interfaces_router.register(r'dhcp/relay', DHCPRelayViewSet, basename='interfaces_dhcp_relays')
# # interfaces_router.register(r'nat/pool', HAClusterViewSet, basename='interfaces_nat_pools')


# # policies subfolder L1
# # objects subfolder L1
# # settings subfolder L1
# # monitor subfolder L1
# # account subfolder L1
# # templates subfolder L1
# # account subfolder L1

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include(dashboard_router.urls)),
#     path('network/', include(network_router.urls)),
#     path('network/', include(sites_router.urls)),
#     path('network/', include(interfaces_router.urls)),
#     path('policies/', include(policies_router.urls)),
#     path('objects/', include(objects_router.urls)),
#     path('settings/', include(settings_router.urls)),
#     path('monitor/', include(monitor_router.urls)),
#     path('templates/', include(templates_router.urls)),
#     path('account/', include(account_router.urls)),

# ]