# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Tenant
# from . import default_settings


# @receiver(post_save, sender=Tenant)
# def tenant_created(sender, instance, created, **kwargs):
#     if created:
#         default_settings.create_objects(instance.id)