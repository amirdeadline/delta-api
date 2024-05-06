# base/views.py
from rest_framework import viewsets
from .models import Tag, Secret, AvailableOverlayIP, BaseModel, CondidateConfig, SnapshotConfig
from .serializers import TagSerializer, SecretSerializer, AvailableOverlayIPSerializer, BaseModelSerializer, CondidateConfigSerializer, SnapshotConfigSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class BaseModelViewSet(viewsets.ModelViewSet):
    serializer_class = BaseModelSerializer
    queryset = BaseModel.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user_id, modified_by=self.request.user_id)
        except Exception as e:
            logger.error(f"Error during object creation: {str(e)}")
            raise ValidationError({'error': 'Error during creation', 'details': str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save(modified_by=self.request.user_id)
        except Exception as e:
            logger.error(f"Error during object update: {str(e)}")
            raise ValidationError({'error': 'Error during update', 'details': str(e)})

    def destroy(self, request, *args, **kwargs):
        try:
            return super(BaseModelViewSet, self).destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error during object deletion: {str(e)}")
            return Response({'error': 'Error during deletion', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SecretViewSet(BaseModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer

class AvailableOverlayIPViewSet(viewsets.ModelViewSet):
    queryset = AvailableOverlayIP.objects.all()
    serializer_class = AvailableOverlayIPSerializer

class CondidateConfigViewSet(BaseModelViewSet):
    queryset = CondidateConfig.objects.all()
    serializer_class = CondidateConfigSerializer

class SnapshotConfigViewSet(BaseModelViewSet):
    queryset = SnapshotConfig.objects.all()
    serializer_class = SnapshotConfigSerializer
