from django.apps import AppConfig

class TenantsAppConfig(AppConfig):
    name = 'tenants_app'

    def ready(self):
        import tenants_app.signals
