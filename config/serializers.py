# config_app/serializers.py
from rest_framework import serializers
from base.serializers import BaseModelSerializer
from .models import CandidateConfig, SnapshotConfig
import logging

logger = logging.getLogger(__name__)

class ConfigBaseSerializer(BaseModelSerializer):
    """"
    This is Serializers for config app inherits attributes from BaseModelSerializers in base app
    """
    pass


class SnapshotConfigSerializer(ConfigBaseSerializer):
    class Meta(ConfigBaseSerializer.Meta):
        model = SnapshotConfig
        exclude = ConfigBaseSerializer.Meta.exclude + ['url']

class CandidateConfigSerializer(ConfigBaseSerializer):
    base_snapshot = serializers.SerializerMethodField(read_only=True)

    class Meta(ConfigBaseSerializer.Meta):
        model = CandidateConfig
        read_only_fields = ConfigBaseSerializer.Meta.read_only_fields + ['base_snapshot','base_path', 'committed_by', 'committed_at']
        exclude = ConfigBaseSerializer.Meta.exclude

    def get_base_snapshot(self, obj):
        if obj.base_snapshot:
            return obj.base_snapshot.object_id
        return None
