# delta_api project urls_tenants.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponseServerError


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/config/', include('base.urls')),
    path('api/v1/resources/', include('resources_app.urls')),
    # path('network/sites/', include('sites_app.urls')),
    # path('network/devices/', include('devices_app.urls')),
    # path('dashboard/', include('dashboard_app.urls')),
    # path('network/', include('network_app.urls')),
    # path('monitor/', include('monitor_app.urls')),
    # path('profiles/', include('profiles_app.urls')),
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

