#config_app.urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantSettingViewSet, SASEInfraSubnetViewSet

router = DefaultRouter()
router.register(r'sase/subnets', SASEInfraSubnetViewSet)
router.register(r'', TenantSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
