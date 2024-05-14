# base/serializers.py
from rest_framework import serializers
from .models import Tag, AvailableOverlayIP, BaseModel, CandidateConfig, SnapshotConfig, TenantSetting
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['key', 'value']

class ErrorHandlingMixin:
    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(f"Validation error: {e.detail}")
            raise ValidationError({'error': 'Validation failed', 'details': e.detail})

class BaseModelSerializer(ErrorHandlingMixin, serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    object_id = serializers.CharField(read_only=True) 
    uuid = serializers.CharField(read_only=True) 
    created_by = serializers.CharField(read_only=True)
    modified_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BaseModel
        exclude = ['id']
        read_only_fields = ['uuid', 'object_id', 'created_at', 'modified_at', 'modified_by', 'created_by']    

    def get_tags(self, obj):
        tags = Tag.objects.filter(object_id=obj.object_id)
        return TagSerializer(tags, many=True).data

    def to_representation(self, instance):
        """
        Modify the output representation to include properly serialized tags data.
        """
        ret = super().to_representation(instance)
        ret['tags'] = self.get_tags(instance)
        return ret
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        self.update_or_create_tags(instance, tags_data)
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        # Always redefine tags on PUT request
        self.redefine_tags(instance, tags_data)
        instance = super().update(instance, validated_data)
        return instance

    def redefine_tags(self, instance, tags_data):
        # Delete all existing tags
        Tag.objects.filter(object_id=instance.object_id).delete()
        # Recreate tags from provided data
        for tag_data in tags_data:
            Tag.objects.create(object_id=instance.object_id, **tag_data)

    def update_or_create_tags(self, instance, tags_data):
        existing_tags = Tag.objects.filter(object_id=str(instance.object_id))
        for tag_data in tags_data:
            tag, _ = Tag.objects.update_or_create(
                object_id=str(instance.object_id),
                key=tag_data['key'],
                defaults={'value': tag_data.get('value', {})}
            )

class SnapshotConfigSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = SnapshotConfig
        exclude = BaseModelSerializer.Meta.exclude + ['path']

class CandidateConfigSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CandidateConfig
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ['base_path', 'committed_by', 'committed_at']
        exclude = BaseModelSerializer.Meta.exclude + ['path']



class AvailableOverlayIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableOverlayIP
        fields = '__all__'




# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         # exclude = ['id']

# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         # exclude = ['id']

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSetting
        # exclude = ['id']

class TenantSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSetting
        fields = ['key', 'value']
        