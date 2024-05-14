# base/views.py
from rest_framework import viewsets
from .models import AvailableOverlayIP, BaseModel, CandidateConfig, SnapshotConfig, TenantSetting
from .serializers import AvailableOverlayIPSerializer, BaseModelSerializer, CandidateConfigSerializer, SnapshotConfigSerializer, TenantSettingSerializer
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that provides default 'create', 'retrieve', 'update', 'partial_update', 'destroy'
    and 'list' actions for models inheriting from BaseModel.
    """
    serializer_class = BaseModelSerializer
    lookup_field = 'object_id'
    # def get_queryset(self):
    #     """
    #     Assuming BaseModel is abstract and you are using this class only through inheritance,
    #     you should override this method in child classes.
    #     """
    #     # return BaseModel.objects.none()  # Return none for safety, override this in child classes.

    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user_id, modified_by=self.request.user_id)
            print(self.request.user_id)
        except Exception as e:
            logger.error(f"Error during object creation: {str(e)}")
            raise APIException({'error': 'Error during creation', 'details': str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save(modified_by=self.request.user_id)
        except Exception as e:
            logger.error(f"Error during object update: {str(e)}")
            raise APIException({'error': 'Error during update', 'details': str(e)})

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error during object deletion: {str(e)}")
            raise APIException({'error': 'Error during deletion', 'details': str(e)})

class SnapshotConfigViewSet(BaseModelViewSet):
    queryset = SnapshotConfig.objects.all()
    serializer_class = SnapshotConfigSerializer

def commit_candidate(candidate):
    """
    This function goes throughh chnages json data and commit all changes to the system, including
    updating databse and push celery or kafka tasks
    later will be fixed!
    """
    return True, "test is good"

class CandidateConfigViewSet(BaseModelViewSet):
    queryset = CandidateConfig.objects.all()
    serializer_class = CandidateConfigSerializer

    @action(detail=True, methods=['put'], url_path='commit')
    def commit(self, request, *args, **kwargs):
        """
        Custom action to commit a CandidateConfig. This uses object_id for lookup.
        """
        candidate = self.get_object()  # This will now use object_id for lookup because of the lookup_field setting
        try:
            # Commit logic here
            candidate.committed = True
            candidate.committed_by = request.user_id
            candidate.committed_at = datetime.now()
            candidate.save()
            return Response({"status": "success", "message": "Commit successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
class TenantSettingViewSet(viewsets.ModelViewSet):
    queryset = TenantSetting.objects.all()
    serializer_class = TenantSettingSerializer

    def create(self, request, *args, **kwargs):
        key = request.data.get('key')
        if TenantSetting.objects.filter(key=key).exists():
            return Response({'error': 'Key already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super(TenantSettingViewSet, self).create(request, *args, **kwargs)

class AvailableOverlayIPViewSet(viewsets.ModelViewSet):
    queryset = AvailableOverlayIP.objects.all()
    serializer_class = AvailableOverlayIPSerializer
    