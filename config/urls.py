#config_app.urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  CandidateConfigViewSet, SnapshotConfigViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateConfigViewSet)
router.register(r'snapshots', SnapshotConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
