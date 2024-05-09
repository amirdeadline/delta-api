#base.urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  AvailableOverlayIPViewSet, CandidateConfigViewSet, SnapshotConfigViewSet, TenantSettingViewSet

router = DefaultRouter()
router.register(r'candidate', CandidateConfigViewSet)
router.register(r'snapshot', SnapshotConfigViewSet)
router.register(r'settings', TenantSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
