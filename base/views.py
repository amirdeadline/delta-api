# base/views.py
from rest_framework import viewsets
from .models import BaseModel
from .serializers import BaseModelSerializer
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

# class AvailableOverlayIPViewSet(viewsets.ModelViewSet):
#     queryset = AvailableOverlayIP.objects.all()
#     serializer_class = AvailableOverlayIPSerializer
    