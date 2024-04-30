# tenants_app/serializers.py
from rest_framework import serializers
from .models import (Product, ProductCategory, License, Region, SCE, SASEController,
                     SDWANController, Contact, Customer, AdminUser, Tenant, Tag,
                     IKEEncryption, IKEHash, IKEDHGroup, IKERPF, ESPEncryption,
                     ESPHash, ESPDHGroup, ESPPFS, RoutingProtocol)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

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

class CustomerSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    admins = AdminUserSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    licenses = LicenseSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ('schema_name', 'tenant_id')  # Make these fields read-only

    def create(self, validated_data):
        # Custom creation logic can be added here if necessary
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom update logic, can ensure schema_name and tenant_id are not updated
        # This is just extra safeguarding; 'read_only_fields' already handles it
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        # Ensure no updates to schema_name or tenant_id here
        return super().update(instance, validated_data)

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