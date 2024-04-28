# tenants_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, TenantViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'tenants', TenantViewSet, basename='tenants')

urlpatterns = [
    path('', include(router.urls)),
]
