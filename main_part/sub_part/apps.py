from django.apps import AppConfig
from django.db.models.signals import post_migrate

class SubPartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sub_part'

    def ready(self):
        from sub_part.signals import created_groups_permissions
        post_migrate.connect(created_groups_permissions, sender=self)
