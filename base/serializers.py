# base/serializers.py
from rest_framework import serializers
from .models import Tag, Secret, AvailableOverlayIP, BaseModel, CandidateConfig, SnapshotConfig, Address, Contact, TenantSetting
from django.core.exceptions import ValidationError
from django.db import transaction
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
    tags = TagSerializer(many=True)

    class Meta:
        model = BaseModel
        exclude = ['id']
        read_only_fields = ['uuid']
        abstract = True

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        self.update_or_create_tags(instance, tags_data)
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        self.update_or_create_tags(instance, tags_data)
        return instance

    def update_or_create_tags(self, instance, tags_data):
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                key=tag_data['key'],
                defaults={'value': tag_data['value']}
            )
            instance.tags.add(tag)

class SecretSerializer(BaseModelSerializer):
    class Meta:
        model = Secret
        exclude = ['id']

class AvailableOverlayIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableOverlayIP
        fields = '__all__'

class CandidateConfigSerializer(BaseModelSerializer):
    class Meta:
        model = CandidateConfig
        exclude = ['id']

class SnapshotConfigSerializer(BaseModelSerializer):
    class Meta:
        model = SnapshotConfig
        exclude = ['id']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['id']

class TenantSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSetting
        exclude = ['id']


        