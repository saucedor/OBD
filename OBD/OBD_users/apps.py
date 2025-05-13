from django.apps import AppConfig


class ObdUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OBD_users'

    def ready(self):
        import OBD_users.signals
