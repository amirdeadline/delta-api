#base.urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import 

router = DefaultRouter()
# router.register(r'addresses', CandidateConfigViewSet)
# router.register(r'addrgroups', SnapshotConfigViewSet)
# router.register(r'zones', TenantSettingViewSet)
# router.register(r'urls', TenantSettingViewSet)
# router.register(r'urlgroups', TenantSettingViewSet)
# router.register(r'applications', TenantSettingViewSet)
# router.register(r'prefixlists', TenantSettingViewSet)
# router.register(r'secrets', TenantSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
