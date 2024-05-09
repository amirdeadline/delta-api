# base/views.py
from rest_framework import viewsets
from .models import AvailableOverlayIP, BaseModel, CandidateConfig, SnapshotConfig, TenantSetting
from .serializers import AvailableOverlayIPSerializer, BaseModelSerializer, CandidateConfigSerializer, SnapshotConfigSerializer, TenantSettingSerializer
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class BaseModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that provides default 'create', 'retrieve', 'update', 'partial_update', 'destroy'
    and 'list' actions for models inheriting from BaseModel.
    """
    # serializer_class = BaseModelSerializer
    # queryset = BaseModel.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user_id, modified_by=self.request.user_id)
        except Exception as e:  # Consider specifying the exception type if possible
            logger.error(f"Error during object creation: {str(e)}")
            raise APIException({'error': 'Error during creation', 'details': str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save(modified_by=self.request.user_id)
        except Exception as e:  # Consider specifying the exception type if possible
            logger.error(f"Error during object update: {str(e)}")
            raise APIException({'error': 'Error during update', 'details': str(e)})

    def destroy(self, request, *args, **kwargs):
        try:
            return super(BaseModelViewSet, self).destroy(request, *args, **kwargs)
        except Exception as e:  # Consider specifying the exception type if possible
            logger.error(f"Error during object deletion: {str(e)}")
            raise APIException({'error': 'Error during deletion', 'details': str(e)})

class AvailableOverlayIPViewSet(viewsets.ModelViewSet):
    queryset = AvailableOverlayIP.objects.all()
    serializer_class = AvailableOverlayIPSerializer

class CandidateConfigViewSet(BaseModelViewSet):
    queryset = CandidateConfig.objects.all()
    serializer_class = CandidateConfigSerializer

class SnapshotConfigViewSet(BaseModelViewSet):
    queryset = SnapshotConfig.objects.all()
    serializer_class = SnapshotConfigSerializer

class TenantSettingViewSet(viewsets.ModelViewSet):
    queryset = TenantSetting.objects.all()
    serializer_class = TenantSettingSerializer

    def create(self, request, *args, **kwargs):
        key = request.data.get('key')
        if TenantSetting.objects.filter(key=key).exists():
            return Response({'error': 'Key already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super(TenantSettingViewSet, self).create(request, *args, **kwargs)