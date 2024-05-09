# tenants_app/serializers.py
from rest_framework import serializers
from .models import (ShareBase, Product, ProductCategory, License, Region, SCE, SASEController,
                     SDWANController, Contact, Customer, AdminUser, Tenant, ShareTag,
                     IKEEncryption, IKEHash, IKEDHGroup, IKERPF, ESPEncryption,
                     InterfaceType, InterfaceRole, VRFRole, LACPHashOption, DeviceModel,
                     ESPHash, ESPDHGroup, ESPPFS, RoutingProtocol, SDWANSoftware)
from django.core.exceptions import ValidationError  # Import ValidationError
import logging

logger = logging.getLogger(__name__)

class ShareTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTag
        fields = ['key', 'value']

class ErrorHandlingMixin:
    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(f"Validation error: {e.detail}")
            raise ValidationError({'error': 'Validation failed', 'details': e.detail})

class SharedBaseModelSerializer(ErrorHandlingMixin, serializers.ModelSerializer):
    tags = ShareTagSerializer(many=True, required=False)
    object_id = serializers.CharField(read_only=True) 
    uuid = serializers.CharField(read_only=True) 
    created_by = serializers.CharField(read_only=True)
    modified_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)  # Ensure created_at is read-only
    modified_at = serializers.DateTimeField(read_only=True)  # Ensure modified_at is read-only

    class Meta:
        model = ShareBase
        exclude = ['id']
        read_only_fields = ['uuid', 'object_id', 'created_at', 'modified_at', 'modified_by', 'created_by']    

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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class SCESerializer(serializers.ModelSerializer):
    class Meta:
        model = SCE
        fields = '__all__'

class SASEControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SASEController
        fields = '__all__'

class SDWANControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDWANController
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class SDWANSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDWANSoftware
        fields = '__all__'

class InterfaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceType
        fields = '__all__'

class InterfaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceRole
        fields = '__all__'

class VRFRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VRFRole
        fields = '__all__'

class LACPHashOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LACPHashOption
        fields = '__all__'

class DeviceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = '__all__'

class IKEEncryptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IKEEncryption
        fields = '__all__'

class IKEHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = IKEHash
        fields = '__all__'

class IKEDHGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IKEDHGroup
        fields = '__all__'

class IKERPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = IKERPF
        fields = '__all__'

class ESPEncryptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESPEncryption
        fields = '__all__'

class ESPHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESPHash
        fields = '__all__'

class ESPDHGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESPDHGroup
        fields = '__all__'

class ESPPFSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESPPFS
        fields = '__all__'

class RoutingProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutingProtocol
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    admins = AdminUserSerializer(many=True, required=False)
    products = ProductSerializer(many=True, required=False)
    licenses = LicenseSerializer(many=True, required=False)
    softwares = SDWANSoftwareSerializer(many=True, required=False)
    tags = ShareTagSerializer(many=True, required=False)
    
    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ('schema_name', 'tenant_id')  # Make these fields read-only

    def create(self, validated_data):
        admins_data = validated_data.pop('admins', [])
        products_data = validated_data.pop('products', [])
        licenses_data = validated_data.pop('licenses', [])
        softwares_data = validated_data.pop('softwares', [])
        tags_data = validated_data.pop('tags', [])
            
        tenant = Tenant.objects.create(**validated_data)

        for admin_data in admins_data:
            admin, created = AdminUser.objects.get_or_create(**admin_data)
            tenant.admins.add(admin)

        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            tenant.products.add(product)

        for license_data in licenses_data:
            license, created = License.objects.get_or_create(**license_data)
            tenant.licenses.add(license)

        for software_data in softwares_data:
            software, created = SDWANSoftware.objects.get_or_create(**software_data)
            tenant.softwares.add(software)

        for tag_data in tags_data:
            tag, created = ShareTag.objects.get_or_create(**tag_data)
            tenant.tags.add(tag)

        return tenant
    def update(self, instance, validated_data):
        # Custom update logic, can ensure schema_name and tenant_id are not updated
        # This is just extra safeguarding; 'read_only_fields' already handles it
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        # Ensure no updates to schema_name or tenant_id here
        return super().update(instance, validated_data)
    

class CustomerSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'