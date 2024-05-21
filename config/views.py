# config_app/views.py
from rest_framework import viewsets
from .models import CandidateConfig, SnapshotConfig
from .serializers import CandidateConfigSerializer, SnapshotConfigSerializer, ConfigBaseSerializer

# from base.models import BaseModel
# from base.serializers import BaseModelSerializer
from base.views import BaseModelViewSet

from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConfigBaseViewSet(BaseModelViewSet):
    """
    A base viewset that provides inherited 'create', 'retrieve', 'update', 'partial_update', 'destroy'
    and 'list' actions for models inheriting from BaseModelViewset.
    """
    serializer_class = ConfigBaseSerializer
    lookup_field = 'object_id'


class SnapshotConfigViewSet(ConfigBaseViewSet):
    queryset = SnapshotConfig.objects.all()
    serializer_class = SnapshotConfigSerializer

def commit_candidate(candidate):
    """
    This function goes throughh chnages json data and commit all changes to the system, including
    updating databse and push celery or kafka tasks
    later will be fixed!
    """
    return True, "test is good"

class CandidateConfigViewSet(ConfigBaseViewSet):
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
