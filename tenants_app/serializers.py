# tenants_app/serializers.py
from rest_framework import serializers
from .models import Customer, Tenant

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ('schema_name', 'tenant_id')  # Make schema_name read only

    def create(self, validated_data):
        # Pop the schema_name field from the validated data
        validated_data.pop('schema_name', None)
        
        # Call super to create the Tenant
        return super().create(validated_data)




        # fields = ['id', 'name', 'description', 'created_on', 'customer_id']

    # def validate(self, attrs):
    #     # Provide a default schema_name if it's not already set
    #     attrs.setdefault('schema_name', 'default')
    #     return attrs

    # def create(self, validated_data):
    #     # Create the tenant without saving it to the database
    #     tenant = Tenant(**validated_data)
    #     tenant.schema_name = f'Tenant_{tenant.schema_name}'
    #     tenant.save()  # Now save it to the database
    #     return tenant