#base.urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecretViewSet, AvailableOverlayIPViewSet, CondidateConfigViewSet, SnapshotConfigViewSet

router = DefaultRouter()
router.register(r'secrets', SecretViewSet)
router.register(r'ips', AvailableOverlayIPViewSet)
router.register(r'candidate', CondidateConfigViewSet)
router.register(r'snapshot', SnapshotConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
