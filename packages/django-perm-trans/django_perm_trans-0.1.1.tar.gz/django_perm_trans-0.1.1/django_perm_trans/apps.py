from django.apps import AppConfig


class DjangoPermTransConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_perm_trans'

    def ready(self):
        from django.db.models.signals import post_init
        from django.contrib.auth.models import Permission
        from django_perm_trans.functions import setup_translations
        post_init.connect(setup_translations, sender=Permission)
