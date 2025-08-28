from django.apps import AppConfig


class SessionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'session'

    def ready(self):
        # ⚡ Importer les signaux ici
        import session.signals
